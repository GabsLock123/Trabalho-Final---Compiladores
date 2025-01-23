# Generated from C.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .CParser import CParser
else:
    from CParser import CParser

# This class defines a complete listener for a parse tree produced by CParser.
class CListener(ParseTreeListener):

    # Enter a parse tree produced by CParser#program.
    def enterProgram(self, ctx:CParser.ProgramContext):
        pass

    # Exit a parse tree produced by CParser#program.
    def exitProgram(self, ctx:CParser.ProgramContext):
        pass


    # Enter a parse tree produced by CParser#directive.
    def enterDirective(self, ctx:CParser.DirectiveContext):
        pass

    # Exit a parse tree produced by CParser#directive.
    def exitDirective(self, ctx:CParser.DirectiveContext):
        pass


    # Enter a parse tree produced by CParser#functionDef.
    def enterFunctionDef(self, ctx:CParser.FunctionDefContext):
        pass

    # Exit a parse tree produced by CParser#functionDef.
    def exitFunctionDef(self, ctx:CParser.FunctionDefContext):
        pass


    # Enter a parse tree produced by CParser#structDef.
    def enterStructDef(self, ctx:CParser.StructDefContext):
        pass

    # Exit a parse tree produced by CParser#structDef.
    def exitStructDef(self, ctx:CParser.StructDefContext):
        pass


    # Enter a parse tree produced by CParser#statement.
    def enterStatement(self, ctx:CParser.StatementContext):
        pass

    # Exit a parse tree produced by CParser#statement.
    def exitStatement(self, ctx:CParser.StatementContext):
        pass


    # Enter a parse tree produced by CParser#block.
    def enterBlock(self, ctx:CParser.BlockContext):
        pass

    # Exit a parse tree produced by CParser#block.
    def exitBlock(self, ctx:CParser.BlockContext):
        pass


    # Enter a parse tree produced by CParser#varDecl.
    def enterVarDecl(self, ctx:CParser.VarDeclContext):
        pass

    # Exit a parse tree produced by CParser#varDecl.
    def exitVarDecl(self, ctx:CParser.VarDeclContext):
        pass


    # Enter a parse tree produced by CParser#assignment.
    def enterAssignment(self, ctx:CParser.AssignmentContext):
        pass

    # Exit a parse tree produced by CParser#assignment.
    def exitAssignment(self, ctx:CParser.AssignmentContext):
        pass


    # Enter a parse tree produced by CParser#ifStatement.
    def enterIfStatement(self, ctx:CParser.IfStatementContext):
        pass

    # Exit a parse tree produced by CParser#ifStatement.
    def exitIfStatement(self, ctx:CParser.IfStatementContext):
        pass


    # Enter a parse tree produced by CParser#whileStatement.
    def enterWhileStatement(self, ctx:CParser.WhileStatementContext):
        pass

    # Exit a parse tree produced by CParser#whileStatement.
    def exitWhileStatement(self, ctx:CParser.WhileStatementContext):
        pass


    # Enter a parse tree produced by CParser#doWhileStatement.
    def enterDoWhileStatement(self, ctx:CParser.DoWhileStatementContext):
        pass

    # Exit a parse tree produced by CParser#doWhileStatement.
    def exitDoWhileStatement(self, ctx:CParser.DoWhileStatementContext):
        pass


    # Enter a parse tree produced by CParser#forStatement.
    def enterForStatement(self, ctx:CParser.ForStatementContext):
        pass

    # Exit a parse tree produced by CParser#forStatement.
    def exitForStatement(self, ctx:CParser.ForStatementContext):
        pass


    # Enter a parse tree produced by CParser#switchStatement.
    def enterSwitchStatement(self, ctx:CParser.SwitchStatementContext):
        pass

    # Exit a parse tree produced by CParser#switchStatement.
    def exitSwitchStatement(self, ctx:CParser.SwitchStatementContext):
        pass


    # Enter a parse tree produced by CParser#breakStatement.
    def enterBreakStatement(self, ctx:CParser.BreakStatementContext):
        pass

    # Exit a parse tree produced by CParser#breakStatement.
    def exitBreakStatement(self, ctx:CParser.BreakStatementContext):
        pass


    # Enter a parse tree produced by CParser#caseLabel.
    def enterCaseLabel(self, ctx:CParser.CaseLabelContext):
        pass

    # Exit a parse tree produced by CParser#caseLabel.
    def exitCaseLabel(self, ctx:CParser.CaseLabelContext):
        pass


    # Enter a parse tree produced by CParser#defaultLabel.
    def enterDefaultLabel(self, ctx:CParser.DefaultLabelContext):
        pass

    # Exit a parse tree produced by CParser#defaultLabel.
    def exitDefaultLabel(self, ctx:CParser.DefaultLabelContext):
        pass


    # Enter a parse tree produced by CParser#caseBlock.
    def enterCaseBlock(self, ctx:CParser.CaseBlockContext):
        pass

    # Exit a parse tree produced by CParser#caseBlock.
    def exitCaseBlock(self, ctx:CParser.CaseBlockContext):
        pass


    # Enter a parse tree produced by CParser#defaultBlock.
    def enterDefaultBlock(self, ctx:CParser.DefaultBlockContext):
        pass

    # Exit a parse tree produced by CParser#defaultBlock.
    def exitDefaultBlock(self, ctx:CParser.DefaultBlockContext):
        pass


    # Enter a parse tree produced by CParser#functionCall.
    def enterFunctionCall(self, ctx:CParser.FunctionCallContext):
        pass

    # Exit a parse tree produced by CParser#functionCall.
    def exitFunctionCall(self, ctx:CParser.FunctionCallContext):
        pass


    # Enter a parse tree produced by CParser#inputOutputStatement.
    def enterInputOutputStatement(self, ctx:CParser.InputOutputStatementContext):
        pass

    # Exit a parse tree produced by CParser#inputOutputStatement.
    def exitInputOutputStatement(self, ctx:CParser.InputOutputStatementContext):
        pass


    # Enter a parse tree produced by CParser#expression.
    def enterExpression(self, ctx:CParser.ExpressionContext):
        pass

    # Exit a parse tree produced by CParser#expression.
    def exitExpression(self, ctx:CParser.ExpressionContext):
        pass


    # Enter a parse tree produced by CParser#argumentList.
    def enterArgumentList(self, ctx:CParser.ArgumentListContext):
        pass

    # Exit a parse tree produced by CParser#argumentList.
    def exitArgumentList(self, ctx:CParser.ArgumentListContext):
        pass


    # Enter a parse tree produced by CParser#paramList.
    def enterParamList(self, ctx:CParser.ParamListContext):
        pass

    # Exit a parse tree produced by CParser#paramList.
    def exitParamList(self, ctx:CParser.ParamListContext):
        pass


    # Enter a parse tree produced by CParser#type.
    def enterType(self, ctx:CParser.TypeContext):
        pass

    # Exit a parse tree produced by CParser#type.
    def exitType(self, ctx:CParser.TypeContext):
        pass



del CParser