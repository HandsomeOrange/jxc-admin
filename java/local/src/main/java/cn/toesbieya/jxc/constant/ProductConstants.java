package cn.toesbieya.jxc.constant;

public class ProductConstants {

    public static class Suffix {
        public static final String SHOPIFY_SUFFIX = ".csv";
    }

    public static class Visible {
        public static final int YES = 1;
        public static final int NO = 0;

    }

    public static final int YES = Visible.YES;
    public static final int NO = Visible.NO;

    public static class ExportStatus {
        public static final int WAITING = 0;
        public static final int SUCCESS = 1;
        public static final int FAIL = -1;
    }

    public static class FromSite {
        public static final String SHOPIFY = "shopify";
        public static final String X = "X";
    }

    public static final String URL_SEPARATOR = ",";
}
