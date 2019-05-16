import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.tree.*;
import java.io.*;
import java.util.*;

public class SolidityWalker extends SolidityBaseListener {

    public static final String[] ruleNames = {
		"sourceUnit", "pragmaDirective", "pragmaName", "pragmaValue", "version", 
		"versionOperator", "versionConstraint", "importDeclaration", "importDirective", 
		"contractDefinition", "inheritanceSpecifier", "contractPart", "stateVariableDeclaration", 
		"usingForDeclaration", "structDefinition", "constructorDefinition", "modifierDefinition", 
		"modifierInvocation", "functionDefinition", "returnParameters", "modifierList", 
		"eventDefinition", "enumValue", "enumDefinition", "parameterList", "parameter", 
		"eventParameterList", "eventParameter", "functionTypeParameterList", "functionTypeParameter", 
		"variableDeclaration", "typeName", "userDefinedTypeName", "mapping", "functionTypeName", 
		"storageLocation", "stateMutability", "block", "statement", "expressionStatement", 
		"ifStatement", "whileStatement", "simpleStatement", "forStatement", "inlineAssemblyStatement", 
		"doWhileStatement", "continueStatement", "breakStatement", "returnStatement", 
		"throwStatement", "emitStatement", "variableDeclarationStatement", "identifierList", 
		"elementaryTypeName", "expression", "primaryExpression", "expressionList", 
		"nameValueList", "nameValue", "functionCallArguments", "functionCall", 
		"assemblyBlock", "assemblyItem", "assemblyExpression", "assemblyCall", 
		"assemblyLocalDefinition", "assemblyAssignment", "assemblyIdentifierOrList", 
		"assemblyIdentifierList", "assemblyStackAssignment", "labelDefinition", 
		"assemblySwitch", "assemblyCase", "assemblyFunctionDefinition", "assemblyFunctionReturns", 
		"assemblyFor", "assemblyIf", "assemblyLiteral", "subAssembly", "tupleExpression", 
		"elementaryTypeNameExpression", "numberLiteral", "identifier"
    };

    StringBuilder tokens;

    public SolidityWalker(StringBuilder tokens) {
        this.tokens = tokens;
    }
    
    public void enterIfStatement(SolidityParser.IfStatementContext ctx) {
        List<Integer> lineSpans = getLineSpan(ctx);
        List<Token> statementTokens = getTokenList(ctx);
        List<String> ancestors = getAncestorList(ctx); 
        //List<Token> contextTokens = getContextList(ctx);
        Collections.reverse(ancestors);
        tokens.append( Arrays.toString(lineSpans.toArray()) + "\t");
        tokens.append( Arrays.toString(ancestors.toArray()) + "\t");
        tokens.append( Arrays.toString(statementTokens.toArray()) + "\n");
        //tokens.append( Arrays.toString(contextTokens.toArray()) + "\n");
    }

    public void enterWhileStatement(SolidityParser.WhileStatementContext ctx) {
        List<Integer> lineSpans = getLineSpan(ctx);
        List<Token> statementTokens = getTokenList(ctx);
        List<String> ancestors = getAncestorList(ctx); 
        //List<Token> contextTokens = getContextList(ctx);
        Collections.reverse(ancestors);
        tokens.append( Arrays.toString(lineSpans.toArray()) + "\t");
        tokens.append( Arrays.toString(ancestors.toArray()) + "\t");
        tokens.append( Arrays.toString(statementTokens.toArray()) + "\n");
        //tokens.append( Arrays.toString(contextTokens.toArray()) + "\n");
    }

    public void enterForStatement(SolidityParser.ForStatementContext ctx) {
        List<Integer> lineSpans = getLineSpan(ctx);
        List<Token> statementTokens = getTokenList(ctx);
        List<String> ancestors = getAncestorList(ctx); 
        //List<Token> contextTokens = getContextList(ctx);
        Collections.reverse(ancestors);
        tokens.append( Arrays.toString(lineSpans.toArray()) + "\t");
        tokens.append( Arrays.toString(ancestors.toArray()) + "\t");
        tokens.append( Arrays.toString(statementTokens.toArray()) + "\n");
        //tokens.append( Arrays.toString(contextTokens.toArray()) + "\n");
    }

    /* 
    public void enterBlock(SolidityParser.BlockContext ctx) {
        List<Token> statementTokens = getTokenList(ctx);
        List<String> ancestors = getAncestorList(ctx); 
        tokens.append( Arrays.toString(ancestors.toArray()) + " ");
        tokens.append( Arrays.toString(statementTokens.toArray()) + "\n");
    }
    */

    public void enterInlineAssemblyStatement(SolidityParser.InlineAssemblyStatementContext ctx) {
        List<Integer> lineSpans = getLineSpan(ctx);
        List<Token> statementTokens = getTokenList(ctx);
        List<String> ancestors = getAncestorList(ctx); 
        //List<Token> contextTokens = getContextList(ctx);
        Collections.reverse(ancestors);
        tokens.append( Arrays.toString(lineSpans.toArray()) + "\t");
        tokens.append( Arrays.toString(ancestors.toArray()) + "\t");
        tokens.append( Arrays.toString(statementTokens.toArray()) + "\n");
        //tokens.append( Arrays.toString(contextTokens.toArray()) + "\n");
    }

    public void enterDoWhileStatement(SolidityParser.DoWhileStatementContext ctx) { 
        List<Integer> lineSpans = getLineSpan(ctx);
        List<Token> statementTokens = getTokenList(ctx);
        List<String> ancestors = getAncestorList(ctx); 
        //List<Token> contextTokens = getContextList(ctx);
        Collections.reverse(ancestors);
        tokens.append( Arrays.toString(lineSpans.toArray()) + "\t");
        tokens.append( Arrays.toString(ancestors.toArray()) + "\t");
        tokens.append( Arrays.toString(statementTokens.toArray()) + "\n");
        //tokens.append( Arrays.toString(contextTokens.toArray()) + "\n");
    }

    public void enterContinueStatement(SolidityParser.ContinueStatementContext ctx) {
        List<Integer> lineSpans = getLineSpan(ctx);
        List<Token> statementTokens = getTokenList(ctx);
        List<String> ancestors = getAncestorList(ctx); 
        //List<Token> contextTokens = getContextList(ctx);
        Collections.reverse(ancestors);
        tokens.append( Arrays.toString(lineSpans.toArray()) + "\t");
        tokens.append( Arrays.toString(ancestors.toArray()) + "\t");
        tokens.append( Arrays.toString(statementTokens.toArray()) + "\n");
        //tokens.append( Arrays.toString(contextTokens.toArray()) + "\n");
    }

    public void enterBreakStatement(SolidityParser.BreakStatementContext ctx) {
        List<Integer> lineSpans = getLineSpan(ctx);
        List<Token> statementTokens = getTokenList(ctx);
        List<String> ancestors = getAncestorList(ctx); 
        //List<Token> contextTokens = getContextList(ctx);
        Collections.reverse(ancestors);
        tokens.append( Arrays.toString(lineSpans.toArray()) + "\t");
        tokens.append( Arrays.toString(ancestors.toArray()) + "\t");
        tokens.append( Arrays.toString(statementTokens.toArray()) + "\n");
        //tokens.append( Arrays.toString(contextTokens.toArray()) + "\n");
    }

    public void enterReturnStatement(SolidityParser.ReturnStatementContext ctx) { 
        List<Integer> lineSpans = getLineSpan(ctx);
        List<Token> statementTokens = getTokenList(ctx);
        List<String> ancestors = getAncestorList(ctx); 
        //List<Token> contextTokens = getContextList(ctx);
        Collections.reverse(ancestors);
        tokens.append( Arrays.toString(lineSpans.toArray()) + "\t");
        tokens.append( Arrays.toString(ancestors.toArray()) + "\t");
        tokens.append( Arrays.toString(statementTokens.toArray()) + "\n");
        //tokens.append( Arrays.toString(contextTokens.toArray()) + "\n");
    }

    public void enterThrowStatement(SolidityParser.ThrowStatementContext ctx) {
        List<Integer> lineSpans = getLineSpan(ctx);
        List<Token> statementTokens = getTokenList(ctx);
        List<String> ancestors = getAncestorList(ctx); 
        //List<Token> contextTokens = getContextList(ctx);
        Collections.reverse(ancestors);
        tokens.append( Arrays.toString(lineSpans.toArray()) + "\t");
        tokens.append( Arrays.toString(ancestors.toArray()) + "\t");
        tokens.append( Arrays.toString(statementTokens.toArray()) + "\n");
        //tokens.append( Arrays.toString(contextTokens.toArray()) + "\n");
    }

    public void enterEmitStatement(SolidityParser.EmitStatementContext ctx) { 
        List<Integer> lineSpans = getLineSpan(ctx);
        List<Token> statementTokens = getTokenList(ctx);
        List<String> ancestors = getAncestorList(ctx); 
        //List<Token> contextTokens = getContextList(ctx);
        Collections.reverse(ancestors);
        tokens.append( Arrays.toString(lineSpans.toArray()) + "\t");
        tokens.append( Arrays.toString(ancestors.toArray()) + "\t");
        tokens.append( Arrays.toString(statementTokens.toArray()) + "\n");
        //tokens.append( Arrays.toString(contextTokens.toArray()) + "\n");
    }

    public void enterSimpleStatement(SolidityParser.SimpleStatementContext ctx) { 
        List<Integer> lineSpans = getLineSpan(ctx);
        List<Token> statementTokens = getTokenList(ctx);
        List<String> ancestors = getAncestorList(ctx); 
        //List<Token> contextTokens = getContextList(ctx);
        Collections.reverse(ancestors);
        tokens.append( Arrays.toString(lineSpans.toArray()) + "\t");
        tokens.append( Arrays.toString(ancestors.toArray()) + "\t");
        tokens.append( Arrays.toString(statementTokens.toArray()) + "\n");
        //tokens.append( Arrays.toString(contextTokens.toArray()) + "\n");
    }


    public static List<Integer> getLineSpan(ParseTree tree) {
        List<Integer> lineSpan = new ArrayList<Integer>(); 
        lineSpan.add( ((ParserRuleContext)tree).getStart().getLine() );
        lineSpan.add( ((ParserRuleContext)tree).getStop().getLine() );
        return lineSpan;
 
    }

    public static List<Token> getTokenList(ParseTree tree) {
        List<Token> tokens = new ArrayList<Token>();
        inOrderTraversal(tokens, tree);
        getContext(tokens, tree);
        return tokens;
    }
    
    public static List<String> getAncestorList(ParseTree tree) {
        List<String> ancestors = new ArrayList<String>();
        getAncestor(ancestors, tree);
        return ancestors;
    }
    
    public static void inOrderTraversal(List<Token> tokens, ParseTree parent) {
        
        for (int i = 0; i < parent.getChildCount(); i++) {
            ParseTree child = parent.getChild(i);
            if (child instanceof TerminalNode) {
                TerminalNode node = (TerminalNode) child;
                tokens.add(node.getSymbol());
                //System.out.println(node.getSymbol());
            } else {
                inOrderTraversal(tokens, child);
            }
        }
    }
    
    public static void getAncestor(List<String> ancestors, ParseTree tree) {
        for (ParseTree current = tree; current != null; current = current.getParent()) {
            if (!(current instanceof RuleNode)) {
                continue;
            }
            RuleNode ruleNode = (RuleNode)current;
            RuleContext ruleContext = ruleNode.getRuleContext();
            int ruleIndex = ruleContext.getRuleIndex();
            String ruleName = ruleNames[ruleIndex];
            ancestors.add(ruleName);
        }
        //System.out.println(ancestors);
    }

    public static void getContext(List<Token> ancestors, ParseTree tree) {

        for (ParseTree current = tree; current != null; current = current.getParent()) {
            if(!(current instanceof RuleNode)) {
                continue;
            }
            RuleNode ruleNode = (RuleNode)current;
            RuleContext ruleContext = ruleNode.getRuleContext();
            int ruleIndex = ruleContext.getRuleIndex();
            String ruleName = ruleNames[ruleIndex];
            if (ruleName == "functionDefinition") {
                // add the function signature into the ancestors
                for (int i = 0; i < current.getChildCount(); i++) {
                    ParseTree child = current.getChild(i);
                    if (child instanceof RuleNode) {
                        RuleNode childRuleNode = (RuleNode)child;
                        String childRuleName = ruleNames[childRuleNode.getRuleContext().getRuleIndex()];         
                        if (childRuleName == "block") {
                            continue;
                        }
                        inOrderTraversal(ancestors, child); 
                    } else if (child instanceof TerminalNode) {
                        TerminalNode childTerminalNode = (TerminalNode) child;
                        ancestors.add(childTerminalNode.getSymbol());
                    } else {
                        continue;
                    }
                }
            } else if (ruleName == "contractDefinition") {
                for (int i = 0; i < current.getChildCount(); i++) {
                    ParseTree child = current.getChild(i);
                    if (child instanceof RuleNode) {
                        RuleNode childRuleNode = (RuleNode)child;
                        String childRuleName = ruleNames[childRuleNode.getRuleContext().getRuleIndex()];         
                        if (childRuleName == "contractPart") {
                            continue;
                        }
                        inOrderTraversal(ancestors, child); 
                    } else if (child instanceof TerminalNode){
                        TerminalNode childTerminalNode = (TerminalNode) child;
                        ancestors.add(childTerminalNode.getSymbol());
                    } else {
                        continue;
                    }
                }
            } else if (ruleName == "ifStatement") {
                // add the condition into the ancestors  
                for (int i = 0; i < current.getChildCount(); i++) {
                    ParseTree child = current.getChild(i);
                    if (child instanceof RuleNode) {
                        RuleNode childRuleNode = (RuleNode)child;
                        String childRuleName = ruleNames[childRuleNode.getRuleContext().getRuleIndex()];         
                        if (childRuleName == "expression") {
                            inOrderTraversal(ancestors, child); 
                        }
                    } else {
                        continue;
                    }
                }
            } else if (ruleName == "whileStatement") {
                // add the condition into the ancestors 
                for (int i = 0; i < current.getChildCount(); i++) {
                    ParseTree child = current.getChild(i);
                    if (child instanceof RuleNode) {
                        RuleNode childRuleNode = (RuleNode)child;
                        String childRuleName = ruleNames[childRuleNode.getRuleContext().getRuleIndex()];         
                        if (childRuleName == "expression") {
                            inOrderTraversal(ancestors, child); 
                        }
                    } else {
                        continue;
                    }
                }
            } else if (ruleName == "forStatement") {
                // add the condition into the ancestors    
                for (int i = 0; i < current.getChildCount(); i++) {
                    ParseTree child = current.getChild(i);
                    if (child instanceof RuleNode) {
                        RuleNode childRuleNode = (RuleNode)child;
                        String childRuleName = ruleNames[childRuleNode.getRuleContext().getRuleIndex()];         
                        if (childRuleName == "expression") {
                            inOrderTraversal(ancestors, child); 
                        }
                    } else {
                        continue;
                    }
                }
            } else if (ruleName == "doWhileStatement") {
                // add the condition into the ancestors
                for (int i = 0; i < current.getChildCount(); i++) {
                    ParseTree child = current.getChild(i);
                    if (child instanceof RuleNode) {
                        RuleNode childRuleNode = (RuleNode)child;
                        String childRuleName = ruleNames[childRuleNode.getRuleContext().getRuleIndex()];         
                        if (childRuleName == "expression") {
                            inOrderTraversal(ancestors, child); 
                        }
                    } else {
                        continue;
                    }
                }
            } else {
                ;
            }
        }
        // System.out.println(ancestors);
    }
}
