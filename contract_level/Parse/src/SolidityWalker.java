import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.tree.*;
import java.io.*;
import java.util.*;

public class SolidityWalker extends SolidityBaseListener {

    StringBuilder tokens;

    public SolidityWalker(StringBuilder tokens) {
        this.tokens = tokens;
    }

	public void enterSourceUnit(SolidityParser.SourceUnitContext ctx) { 
        List<Token> sourceUnitTokens = getTokenList(ctx);
        List<Integer> lineSpans = getLineSpan(ctx);
        tokens.append( Arrays.toString(lineSpans.toArray()) + "\t");

        tokens.append( Arrays.toString(sourceUnitTokens.toArray()) + "\n");
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
        return tokens;
    }

    public static void inOrderTraversal(List<Token> tokens, ParseTree parent) {
        
        for (int i = 0; i < parent.getChildCount(); i++) {
            ParseTree child = parent.getChild(i);
            if (child instanceof TerminalNode) {
                TerminalNode node = (TerminalNode) child;
                tokens.add(node.getSymbol());
                // System.out.println(node.getSymbol());
            } else {
                inOrderTraversal(tokens, child);
            }
        }
    }
}

