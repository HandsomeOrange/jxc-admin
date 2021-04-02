package cn.toesbieya.jxc.util;

import org.apache.commons.lang3.StringUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URL;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Base64;

public class FileUtils {

    private static final Logger logger = LoggerFactory.getLogger(FileUtils.class);

    private static final String SAVE_PATH = savePath();

    public static void main(String[] args) {

    }

    public static String collectProducts(String collectionUrl, String fileName, Integer exportType) {
        String res = StringUtils.EMPTY;
        try {
            res = exec(collectionUrl, getFileRealPath(fileName), String.valueOf(exportType));
//            res = StringUtils.contains(result, "success");
        } catch (Exception e) {
            logger.error("collect product {} error", collectionUrl, e);
        }
        return res;
    }

    public static String getFileContent(String fileName) {
        try {
            File f = new File(getFileRealPath(fileName));
            if (!f.exists()) {
                return null;
            }
            byte[] contents = Files.readAllBytes(Paths.get(getFileRealPath(fileName)));
//            return new String(contents);
            return Base64.getEncoder().encodeToString(contents);
        } catch (IOException e) {
            e.printStackTrace();
        }
        return null;
    }


    public static String getFileRealPath(String fileName) {
        return getSavePath() + fileName;
    }

    public static String getSavePath() {
        return SAVE_PATH;
    }

    private static String savePath() {
        String path = FileUtils.class.getClassLoader().getResource("export/1.csv").getPath();
        return StringUtils.substringBeforeLast(path.substring(1), "/") + File.separator;
    }

    private static String pythonUrl() {
        URL resource = FileUtils.class.getClassLoader().getResource("shopify-python-scraping/shopify.py");
        return resource != null ? resource.getPath().substring(1) : StringUtils.EMPTY;
    }

    private static String exec(String collectionsUrl, String outputFile, String exportType) throws IOException, InterruptedException {
        String[] params = new String[]{"python", pythonUrl(), collectionsUrl, outputFile, exportType};
        System.out.println(StringUtils.join(params," "));
        Process pr = Runtime.getRuntime().exec(params);
        BufferedReader in = new BufferedReader(new InputStreamReader(pr.getInputStream()));
        String line;
        StringBuilder result = new StringBuilder();
        while ((line = in.readLine()) != null) {
            result.append(line);
        }
        in.close();
        pr.waitFor();
        return result.toString();
    }


}
