import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.tree.*;
import java.io.*;

public class Tokenize{
    
    public static String getParseString(String sourcePath) throws IOException {

        InputStream is = new FileInputStream( sourcePath );
        ANTLRInputStream input = new ANTLRInputStream(is);

        SolidityLexer lexer = new SolidityLexer(input);
        CommonTokenStream tokens = new CommonTokenStream(lexer);

        tokens.fill();
        SolidityParser parser = new SolidityParser(tokens);
        ParseTree tree = parser.sourceUnit();
       
        /* Extract Function Tokens */
        ParseTreeWalker walker = new ParseTreeWalker(); 
        StringBuilder contractTokens = new StringBuilder();
        walker.walk(new SolidityWalker(contractTokens), tree);
        
        String result = contractTokens.toString().trim();
        System.out.println(result);
        return result;
        //return contractTokens.toString().trim();

    }
   

    public static void main(String[] args) throws IOException {

        String sourcePath = args[0];
        String targetPath = args[1];
        System.out.println(sourcePath);
        System.out.println(targetPath);
        Tokenize tok = new Tokenize(); 
        String parseResult = tok.getParseString(sourcePath);

        BufferedWriter output = null;
        try{
            File file = new File(targetPath + "parse_result");
            output = new BufferedWriter(new FileWriter(file));
            output.write(parseResult);
        } catch (IOException e) {
            e.printStackTrace();
        } finally{
            if(output != null) {
                output.close();
            }
        }
        
    }
}
