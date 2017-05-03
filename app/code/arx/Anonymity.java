import java.io.*;
import java.nio.charset.Charset;
import java.text.DecimalFormat;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

import org.deidentifier.arx.ARXAnonymizer;
import org.deidentifier.arx.ARXConfiguration;
import org.deidentifier.arx.ARXResult;
import org.deidentifier.arx.AttributeType;
import org.deidentifier.arx.Data;
import org.deidentifier.arx.DataHandle;
import org.deidentifier.arx.DataType;
import org.deidentifier.arx.ARXLattice.ARXNode;
import org.deidentifier.arx.aggregates.HierarchyBuilderIntervalBased;
import org.deidentifier.arx.aggregates.HierarchyBuilderRedactionBased;
import org.deidentifier.arx.aggregates.HierarchyBuilderRedactionBased.Order;
import org.deidentifier.arx.criteria.KAnonymity;
import org.deidentifier.arx.aggregates.HierarchyBuilderIntervalBased.Range;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

public class Anonymity {

    @SuppressWarnings("deprecation")
    public static void main(String[] args) throws IOException {
        // args 0: original dataset path
        // args 1: json configuration file path
        // args 2: aonn dataset path

        Data data = Data.create(new File(args[0]), Charset.defaultCharset(), ',');

        int k = parseConf(data, args[1], args[0]);
//        data.getDefinition().parseConf("Combined OD1", AttributeType.IDENTIFYING_ATTRIBUTE);
//        data.getDefinition().parseConf("Death Date", AttributeType.IDENTIFYING_ATTRIBUTE);
//        data.getDefinition().parseConf("Race", AttributeType.INSENSITIVE_ATTRIBUTE);
//        data.getDefinition().parseConf("Case Dispo", AttributeType.INSENSITIVE_ATTRIBUTE);
//        data.getDefinition().parseConf("Case Dispo", AttributeType.SENSITIVE_ATTRIBUTE);
//        data.getDefinition().parseConf("Age", AgeBuilder);
//        data.getDefinition().parseConf("Incident Zip", ZIPBuilder);
//        data.getDefinition().parseConf("Decedent Zip", ZIPBuilder);


        ARXAnonymizer anonymizer = new ARXAnonymizer();
        ARXConfiguration config = ARXConfiguration.create();
        config.addPrivacyModel(new KAnonymity(k));
        config.setMaxOutliers(0d);
        ARXResult result = anonymizer.anonymize(data, config);

        // Print info
        printResult(result, data);

        // Process results
//        System.out.println(" - Transformed data:");
//        Iterator<String[]> transformed = result.getOutput(false).iterator();
//        while (transformed.hasNext()) {
//            System.out.print("   ");
//            System.out.println(Arrays.toString(transformed.next()));
//        }

        DataHandle handle = result.getOutput(false);
        saveFile(result, args[2]);
        //handle.save(new File(args[2]), ',');

        /*ARXConfiguration config = ARXConfiguration.create();
        config.addCriterion(new KAnonymity(5));
        config.setMaxOutliers(0.02d);
        data.getDefinition().parseConf("disease", AttributeType.SENSITIVE_ATTRIBUTE);
        ARXAnonymizer anonymizer = new ARXAnonymizer();
        ARXResult result = anonymizer.anonymize(data, config);
        DataHandle handle = result.getOutput();
        handle.save(new File("result.csv"), '\t');*/
    }


    private static void saveFile(ARXResult result, String file) {
        PrintWriter writer = null;
        try {
            writer = new PrintWriter(file, "UTF-8");
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
        }
        Iterator<String[]> transformed = result.getOutput(false).iterator();
        while (transformed.hasNext()) {
            StringBuilder line = new StringBuilder();
            for (String s : transformed.next()) {
                StringBuilder sb = new StringBuilder();
                if (s.endsWith("[")) {
                    sb.append(s.substring(0, s.length() - 1))
                            .append("]");
                    s = sb.toString().replace(", ", "-");
                }
                line.append(s)
                        .append(",");
            }
            String record = line.toString().substring(0, line.toString().length() - 1);
            writer.println(record);
        }
        writer.close();
    }

    /**
     * parse the conf file, return k and set all the attr
     *
     * @param data
     * @param jsonPath
     * @return k
     */
    private static int parseConf(Data data, String jsonPath, String datasetPath) {
        int rstK = -1;
        JSONParser parser = new JSONParser();

        try {
            JSONObject jsonObject = (JSONObject) parser.parse(new FileReader(jsonPath));
            rstK = Integer.parseInt((String) jsonObject.get("k"));

            HierarchyBuilderRedactionBased<?> suppressionBuilder = HierarchyBuilderRedactionBased.create(Order.RIGHT_TO_LEFT,
                    Order.RIGHT_TO_LEFT,
                    ' ',
                    '*');

            HierarchyBuilderIntervalBased<Long> AgeBuilder = HierarchyBuilderIntervalBased.create(
                    DataType.INTEGER,
                    new Range<Long>(0l, 0l, 0l),
                    new Range<Long>(99l, 99l, 99l));
            AgeBuilder.setAggregateFunction(DataType.INTEGER.createAggregate().createIntervalFunction(true, false));
            AgeBuilder.addInterval(0l, 15l);
            AgeBuilder.addInterval(15l, 30l);
            AgeBuilder.addInterval(30l, 45l);
            AgeBuilder.addInterval(45l, 60l);
            AgeBuilder.getLevel(0).addGroup(2);
            AgeBuilder.getLevel(1).addGroup(3);

            if (jsonObject.containsKey("sensitive")) {
                for (Object col : (JSONArray) jsonObject.get("sensitive")) {
                    data.getDefinition().setAttributeType((String) col, AttributeType.INSENSITIVE_ATTRIBUTE);
                }
            }
            if (jsonObject.containsKey("insensitive")) {
                for (Object col : (JSONArray) jsonObject.get("insensitive")) {
                    data.getDefinition().setAttributeType((String) col, AttributeType.INSENSITIVE_ATTRIBUTE);
                }
            }
            if (jsonObject.containsKey("identifying")) {
                for (Object col : (JSONArray) jsonObject.get("identifying")) {
                    data.getDefinition().setAttributeType((String) col, AttributeType.QUASI_IDENTIFYING_ATTRIBUTE);
                }
            }
            if (jsonObject.containsKey("numericgeneralization")) {
                for (Object col : (JSONArray) jsonObject.get("numericgeneralization")) {
                    data.getDefinition().setAttributeType((String) col, buildnumGenBuilder(datasetPath, (String) col));
                }
            }
            if (jsonObject.containsKey("suppression")) {
                for (Object col : (JSONArray) jsonObject.get("suppression")) {
                    data.getDefinition().setAttributeType((String) col, suppressionBuilder);
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        } catch (ParseException e) {
            e.printStackTrace();
        }

        return rstK;
    }

    protected static void printResult(final ARXResult result, final Data data) {

        // Print time
        final DecimalFormat df1 = new DecimalFormat("#####0.00");
        final String sTotal = df1.format(result.getTime() / 1000d) + "s";
        System.out.println(" - Time needed: " + sTotal);

        // Extract
        final ARXNode optimum = result.getGlobalOptimum();
        final List<String> qis = new ArrayList<String>(data.getDefinition().getQuasiIdentifyingAttributes());

        if (optimum == null) {
            System.out.println(" - No solution found!");
            return;
        }

        // Initialize
        final StringBuffer[] identifiers = new StringBuffer[qis.size()];
        final StringBuffer[] generalizations = new StringBuffer[qis.size()];
        int lengthI = 0;
        int lengthG = 0;
        for (int i = 0; i < qis.size(); i++) {
            identifiers[i] = new StringBuffer();
            generalizations[i] = new StringBuffer();
            identifiers[i].append(qis.get(i));
            generalizations[i].append(optimum.getGeneralization(qis.get(i)));
            if (data.getDefinition().isHierarchyAvailable(qis.get(i)))
                generalizations[i].append("/").append(data.getDefinition().getHierarchy(qis.get(i))[0].length - 1);
            lengthI = Math.max(lengthI, identifiers[i].length());
            lengthG = Math.max(lengthG, generalizations[i].length());
        }

        // Padding
        for (int i = 0; i < qis.size(); i++) {
            while (identifiers[i].length() < lengthI) {
                identifiers[i].append(" ");
            }
            while (generalizations[i].length() < lengthG) {
                generalizations[i].insert(0, " ");
            }
        }

        String ls = String.format("%.3f", Double.parseDouble(result.getGlobalOptimum().getLowestScore().toString()));
        String hs = String.format("%.3f", Double.parseDouble(result.getGlobalOptimum().getHighestScore().toString()));
        // Print
        System.out.println(" - Information loss: " + ls + " / " + hs);
        System.out.println(" - Optimal generalization");
        for (int i = 0; i < qis.size(); i++) {
            System.out.println("   * " + identifiers[i] + ": " + generalizations[i]);
        }
        System.out.println(" - Statistics");
        System.out.println(result.getOutput(result.getGlobalOptimum(), false).getStatistics().getEquivalenceClassStatistics());
    }


    private static HierarchyBuilderIntervalBased<Long> buildnumGenBuilder(String path, String colName)
            throws NumberFormatException {

        long mean = 0;
        long std = 0;
        long max = Long.MIN_VALUE;
        long min = Long.MAX_VALUE;

        try (BufferedReader br = new BufferedReader(new FileReader(path))) {
            String line;
            int colNum = -1;
            if ((line = br.readLine()) != null) {
                String[] parts = line.split(",");
                for (int i = 0; i < parts.length; i++) {
                    if (parts[i].equalsIgnoreCase(colName)) {
                        colNum = i;
                        break;
                    }
                }
            }

            if (colNum == -1) return null;

            long sum = 0;
            List<Long> list = new ArrayList<>();
            while ((line = br.readLine()) != null) {
                if (line.equalsIgnoreCase("")) continue;
                // use comma as separator
                String[] parts = line.split(",");
                long val = Long.parseLong(parts[colNum]);
                list.add(val);
                sum += val;
            }

            mean = sum / list.size();

            for (long l : list) {
                std += (l - mean) * (l - mean);
                max = Math.max(max, l);
                min = Math.min(min, l);
            }
            std = (long) Math.sqrt(std * 1.0 / list.size());

        } catch (IOException e) {
            e.printStackTrace();
        }

        long interval = Math.max(std, 1);

        HierarchyBuilderIntervalBased<Long> numericGeneralizationBuilder = HierarchyBuilderIntervalBased.create(
                DataType.INTEGER,
                new Range<Long>(min, min, min),
                new Range<Long>(max + 1, max + 1, max + 1));
        numericGeneralizationBuilder.setAggregateFunction(DataType.INTEGER.createAggregate().createIntervalFunction(true, false));
        numericGeneralizationBuilder.addInterval(min, min + interval);
        numericGeneralizationBuilder.getLevel(0).addGroup(2);
        numericGeneralizationBuilder.getLevel(1).addGroup(3);
        return numericGeneralizationBuilder;
    }

}
