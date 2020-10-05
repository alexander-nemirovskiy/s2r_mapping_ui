package it.polimi;

import com.sun.tools.xjc.api.ErrorListener;
import com.sun.tools.xjc.api.S2JJAXBModel;
import com.sun.tools.xjc.api.SchemaCompiler;
import com.sun.tools.xjc.api.XJC;
import org.xml.sax.InputSource;

import org.apache.commons.cli.*;
import java.io.File;
import java.io.FileInputStream;
import com.sun.codemodel.*;
import org.xml.sax.SAXParseException;


public class JaxbApp
{
    public static void main( String[] args ) {
        System.out.println("Starting generation...");
        Options options = new Options();

        Option inputFile = new Option("input", "inputFile", true, "input xsd absolute file path");
        inputFile.setRequired(true);
        options.addOption(inputFile);

        Option outputFolder = new Option("folder", "outputFolder", true, "output folder for generated sources");
        outputFolder.setRequired(true);
        options.addOption(outputFolder);

        CommandLineParser parser = new DefaultParser();
        HelpFormatter formatter = new HelpFormatter();
        CommandLine cmd = null;

        try {
            cmd = parser.parse(options, args);
            System.out.println("Command invoked: " + cmd.toString());
        } catch (ParseException e) {
            System.out.println(e.getMessage());
            formatter.printHelp("utility-name", options);

            System.exit(1);
        }

        String inputFilePath = cmd.getOptionValue("input");
        String outputFolderPath = cmd.getOptionValue("folder");

        try {
            System.out.println("Schema generation for " + inputFilePath);
            System.out.println("Output location " + outputFolderPath);
            generateFromSchema(inputFilePath, outputFolderPath);
        } catch (Exception e) {
            System.out.println(e.getMessage());
            System.exit(1);
        }
        System.out.println("Generation ended!");
        System.exit(0);
    }

    /**
     * Generates JCodeModel and stores it for future annotation and final build/write down to targetPath
     *
     * @throws Exception failure during model generation
     */
    public static void generateFromSchema(String xsdSchemaPath, String outputFolderPath) throws Exception {
        // Setup schema compiler
        SchemaCompiler sc = XJC.createSchemaCompiler();
        sc.setErrorListener(new ErrorListener() {
            @Override
            public void error(SAXParseException e) {
                e.printStackTrace();

            }

            @Override
            public void fatalError(SAXParseException e) {

            }

            @Override
            public void warning(SAXParseException e) {

            }

            @Override
            public void info(SAXParseException e) {

            }

        });

        // Setup SAX InputSource
        File schemaFile = new File(xsdSchemaPath);
        InputSource is = new InputSource(new FileInputStream(schemaFile));
        is.setSystemId(schemaFile.getAbsolutePath());

        // Parse & build
        sc.parseSchema(is);
        sc.setDefaultPackageName("java_classes");
        S2JJAXBModel model = sc.bind();
        if (model == null){
            throw new Exception("No model has been generated!");
        }
        final JCodeModel jcm = model.generateCode(null, null);
        jcm.build(new File(outputFolderPath));
    }
}
