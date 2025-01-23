grammar C;

// Regras principais
program : (directive | functionDef | structDef | statement)* EOF ;

directive 
    : '#include' IncludeFile
    | '#define' Identifier expression
    ;

// Inclui arquivos como <stdio.h> ou "file.h"
IncludeFile
    : '<' ~[<>]+ '>'       // Para arquivos delimitados por < e >
    ;

functionDef 
    : type Identifier '(' paramList? ')' block
    ;

structDef 
    : 'struct' Identifier '{' varDecl* '}' ';'
    ;

statement 
    : varDecl
    | assignment
    | ifStatement
    | whileStatement
    | doWhileStatement
    | forStatement
    | switchStatement
    | functionCall ';'
    | inputOutputStatement ';'
    | ';'
    | block
    | breakStatement  
    | 'return' expression? ';'
    ;

block 
    : '{' statement* '}'
    ;

varDecl 
    : type Identifier ('=' expression)? ';'
    ;

assignment 
    : Identifier '=' expression ';'
    ;

ifStatement 
    : 'if' '(' expression ')' statement ('else' statement)?
    ;

whileStatement 
    : 'while' '(' expression ')' statement
    ;

doWhileStatement 
    : 'do' statement 'while' '(' expression ')' ';'
    ;

forStatement 
    : 'for' '(' (varDecl | assignment)? ';' expression? ';' assignment? ')' statement
    ;

switchStatement 
    : 'switch' '(' expression ')' '{' (caseBlock | defaultBlock)* '}'
    ;

breakStatement
    : 'break' ';'
    ;

caseLabel 
    : 'case' expression ':' 
    ;

defaultLabel 
    : 'default' ':' 
    ;

caseBlock
    : caseLabel statement* breakStatement?
    ;

defaultBlock
    : defaultLabel statement* breakStatement?
    ;

functionCall 
    : Identifier '(' argumentList? ')'
    ;

inputOutputStatement 
    : 'printf' '(' StringLiteral (',' expression)* ')'
    | 'scanf' '(' StringLiteral (',' '&' Identifier)* ')'
    | 'puts' '(' StringLiteral ')'
    | 'gets' '(' Identifier ')'
    ;

// Expressões
expression 
    : '(' expression ')'
    | '-' expression
    | expression ('*' | '/' | '%') expression
    | expression ('+' | '-') expression
    | expression ('<' | '<=' | '>' | '>=') expression
    | expression ('==' | '!=') expression
    | expression ('&&' | '||') expression
    | Identifier
    | Number
    | StringLiteral
    | CharLiteral
    ;

argumentList 
    : expression (',' expression)*
    ;

paramList 
    : type Identifier (',' type Identifier)*
    ;

// Tipos de variáveis
type 
    : 'int'
    | 'float'
    | 'double'
    | 'long double'
    | 'char'
    | 'short'
    | 'long'
    | 'unsigned'
    | 'unsigned char'
    | 'unsigned int'
    | 'unsigned short'
    | 'unsigned long'
    | 'long long'
    | 'unsigned long long'
    ;

// Tokens
Number 
    : [0-9]+ ('.' [0-9]+)?
    ;

CharLiteral
    : '\'' ~[\r\n'] '\''
    ;

StringLiteral
    : '"' (ESCAPED_CHAR | ~["\\])* '"'
    | '"' (~["\\] | '\\' .)* '"'
    ;

fragment ESCAPED_CHAR
    : '\\' ["\\/bfnrt]   // Escapes básicos
    | '\\u' HEX HEX HEX HEX // Unicode
    ;

fragment HEX
    : [0-9a-fA-F]
    ;

Identifier 
    : [a-zA-Z_] [a-zA-Z0-9_]*
    ;

// Espaços em branco e comentários
WS 
    : [ \t\r\n]+ -> skip
    ;

COMMENT 
    : '//' ~[\r\n]* -> skip
    ;

MULTILINE_COMMENT 
    : '/*' .*? '*/' -> skip
    ;
