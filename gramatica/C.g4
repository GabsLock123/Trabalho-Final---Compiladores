grammar C;

// Regras principais
program : (directive | functionDef | structDef | unionDef | statement)* EOF ;

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

unionDef 
    : 'union' Identifier '{' varDecl* '}' ';'
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

returnStatement 
    : 'return' expression? ';'
    ;

block 
    : '{' statement* '}'
    ;

varDecl 
    : type Identifier arraySize? ('=' init)? ';'
    ;

arraySize
    : '[' (Number)? ']'
    ;

init 
    : expression
    | initializerList
    ;

// Lista de inicializadores: { expr, expr, ... }
initializerList 
    : '{' expression (',' expression)* '}'
    ;

assignment 
    : (Identifier ('.' Identifier)*) '=' expression ';'
    | Identifier '[' expression ']' '=' expression ';'
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

forHeaderAssignment
    : Identifier '=' expression
    ;

forStatement 
    : 'for' '(' (varDecl | forHeaderAssignment)? ';' expression? ';' forHeaderAssignment? ')' statement
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

scanfParam
    : Identifier ('[' expression ']')?
    ;

inputOutputStatement 
    : 'printf' '(' StringLiteral (',' expression)* ')'
    | 'scanf' '(' StringLiteral (',' '&' scanfParam)* ')'
    | 'gets' '(' Identifier ')'
    | 'puts' '(' (StringLiteral | expression) ')'
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
    | expression '.' Identifier
    | Identifier ('[' expression ']')*
    | functionCall
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
    | 'struct' Identifier
    | 'union' Identifier
    | 'void'
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
