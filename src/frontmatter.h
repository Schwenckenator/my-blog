#ifndef frontmatter_h
#define frontmatter_h

typedef enum {
    TOKEN_TRIPLE_DASH,
    TOKEN_KEY,
    TOKEN_STRING,
    TOKEN_MINUS,
    TOKEN_NEWLINE,
    TOKEN_ERROR,
    TOKEN_EOF,
} TokenType;

typedef struct {
    TokenType type;
    const char *start;
    int length;
} Token;

void init_scanner(const char *source);
Token scan_token();

#endif
