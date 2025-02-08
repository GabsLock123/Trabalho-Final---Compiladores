# Generated from C.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .CParser import CParser
else:
    from CParser import CParser

# This class defines a complete generic visitor for a parse tree produced by CParser.

class CVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by CParser#program.
    def visitProgram(self, ctx:CParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#directive.
    def visitDirective(self, ctx:CParser.DirectiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#functionDef.
    def visitFunctionDef(self, ctx:CParser.FunctionDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#structDef.
    def visitStructDef(self, ctx:CParser.StructDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#unionDef.
    def visitUnionDef(self, ctx:CParser.UnionDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#statement.
    def visitStatement(self, ctx:CParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#returnStatement.
    def visitReturnStatement(self, ctx:CParser.ReturnStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#block.
    def visitBlock(self, ctx:CParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#varDecl.
    def visitVarDecl(self, ctx:CParser.VarDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#arraySize.
    def visitArraySize(self, ctx:CParser.ArraySizeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#assignment.
    def visitAssignment(self, ctx:CParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#ifStatement.
    def visitIfStatement(self, ctx:CParser.IfStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#whileStatement.
    def visitWhileStatement(self, ctx:CParser.WhileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#doWhileStatement.
    def visitDoWhileStatement(self, ctx:CParser.DoWhileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#forHeaderAssignment.
    def visitForHeaderAssignment(self, ctx:CParser.ForHeaderAssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#forStatement.
    def visitForStatement(self, ctx:CParser.ForStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#switchStatement.
    def visitSwitchStatement(self, ctx:CParser.SwitchStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#breakStatement.
    def visitBreakStatement(self, ctx:CParser.BreakStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#caseLabel.
    def visitCaseLabel(self, ctx:CParser.CaseLabelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#defaultLabel.
    def visitDefaultLabel(self, ctx:CParser.DefaultLabelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#caseBlock.
    def visitCaseBlock(self, ctx:CParser.CaseBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#defaultBlock.
    def visitDefaultBlock(self, ctx:CParser.DefaultBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#functionCall.
    def visitFunctionCall(self, ctx:CParser.FunctionCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#inputOutputStatement.
    def visitInputOutputStatement(self, ctx:CParser.InputOutputStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#expression.
    def visitExpression(self, ctx:CParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#argumentList.
    def visitArgumentList(self, ctx:CParser.ArgumentListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#paramList.
    def visitParamList(self, ctx:CParser.ParamListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#type.
    def visitType(self, ctx:CParser.TypeContext):
        return self.visitChildren(ctx)



del CParser