#include "frontmatter.h"
#include <iterator>
#include <stdbool.h>
#include <string.h>

typedef struct {
    const char *start;
    const char *current;
} Scanner;

Scanner scanner;

void init_scanner(const char *source) {
    scanner.start = source;
    scanner.current = source;
}

static bool is_at_end() { return *scanner.current == '\0'; }

static Token make_token(TokenType type) {
    Token token;
    token.type = type;
    token.start = scanner.start;
    token.length = (int)(scanner.current - scanner.start);
    return token;
}

static Token error_token(const char *message) {
    Token token;
    token.type = TOKEN_ERROR;
    token.start = message;
    token.length = (int)strlen(message);
}

static char advance() {
    scanner.current++;
    return scanner.current[-1];
}

static bool peek_match(const char expected) {
    if (is_at_end())
        return false;
    if (*scanner.current != expected)
        return false;
    return true;
}

static bool peek_next_match(const char expected) {
    if (is_at_end())
        return false;
    if (scanner.current[1] != expected)
        return false;
    return true;
}

static Token string() {
    while (!peek_match('\n') && !is_at_end()) {
        advance();
    }
    return make_token(TOKEN_STRING);
}

Token scan_token() {
    // Set the start of the token to the current positon
    scanner.start = scanner.current;

    if (is_at_end())
        return make_token(TOKEN_EOF);

    char c = advance();

    switch (c) {
    case '-':
        if (peek_match('-') && peek_next_match('-')) {
            // Frontmatter is either starting or finishing
            advance();
            advance();
            return make_token(TOKEN_TRIPLE_DASH);
        }
    }

    return error_token("Unexpected character.");
}
