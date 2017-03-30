import java.io.File;
import java.io.IOException;
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

import cern.colt.Arrays;

public class Anonymity {

    @SuppressWarnings("deprecation")
    public static void main(String[] args) throws IOException {
        Data data = Data.create(new File("od2016.csv"), Charset.defaultCharset(), ',');
        HierarchyBuilderRedactionBased<?> builder2 = HierarchyBuilderRedactionBased.create(Order.RIGHT_TO_LEFT,
                Order.RIGHT_TO_LEFT,
                ' ',
                '*');
        HierarchyBuilderIntervalBased<Long> builder1 = HierarchyBuilderIntervalBased.create(
                DataType.INTEGER,
                new Range<Long>(0l,0l,0l),
                new Range<Long>(99l,99l,99l));
        builder1.setAggregateFunction(DataType.INTEGER.createAggregate().createIntervalFunction(true, false));
        builder1.addInterval(0l, 15l);
        builder1.addInterval(15l, 30l);
        builder1.addInterval(30l, 45l);
        builder1.addInterval(45l, 60l);
        builder1.getLevel(0).addGroup(2);
        builder1.getLevel(1).addGroup(3);
        data.getDefinition().setAttributeType("Combined OD1", AttributeType.IDENTIFYING_ATTRIBUTE);
        data.getDefinition().setAttributeType("Death Date", AttributeType.IDENTIFYING_ATTRIBUTE);
        data.getDefinition().setAttributeType("Race", AttributeType.INSENSITIVE_ATTRIBUTE);
        data.getDefinition().setAttributeType("Case Dispo", AttributeType.INSENSITIVE_ATTRIBUTE);
        data.getDefinition().setAttributeType("Age", builder1);
        data.getDefinition().setAttributeType("Incident Zip", builder2);
        data.getDefinition().setAttributeType("Decedent Zip", builder2);
        ARXAnonymizer anonymizer = new ARXAnonymizer();
        ARXConfiguration config = ARXConfiguration.create();
        config.addPrivacyModel(new KAnonymity(5));
        config.setMaxOutliers(0d);
        ARXResult result = anonymizer.anonymize(data, config);

        // Print info
        printResult(result, data);

        // Process results
        System.out.println(" - Transformed data:");
        Iterator<String[]> transformed = result.getOutput(false).iterator();
        while (transformed.hasNext()) {
            System.out.print("   ");
            System.out.println(Arrays.toString(transformed.next()));
        }
        /*ARXConfiguration config = ARXConfiguration.create();
        config.addCriterion(new KAnonymity(5));
        config.setMaxOutliers(0.02d);
        data.getDefinition().setAttributeType("disease", AttributeType.SENSITIVE_ATTRIBUTE);
        ARXAnonymizer anonymizer = new ARXAnonymizer();
        ARXResult result = anonymizer.anonymize(data, config);
        DataHandle handle = result.getOutput();
        handle.save(new File("result.csv"), '\t');*/
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

        // Print
        System.out.println(" - Information loss: " + result.getGlobalOptimum().getLowestScore() + " / " + result.getGlobalOptimum().getHighestScore());
        System.out.println(" - Optimal generalization");
        for (int i = 0; i < qis.size(); i++) {
            System.out.println("   * " + identifiers[i] + ": " + generalizations[i]);
        }
        System.out.println(" - Statistics");
        System.out.println(result.getOutput(result.getGlobalOptimum(), false).getStatistics().getEquivalenceClassStatistics());
    }
}
