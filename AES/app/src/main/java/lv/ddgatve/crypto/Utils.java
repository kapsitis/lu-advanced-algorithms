package lv.ddgatve.crypto;


//import android.util.Log;

public class Utils {

    // Fields to support logging to a circular buffer...

    private static int maxLogLines = 32;            // power of two
    private static int indexMask = maxLogLines - 1;

    private static String[][] logLines = new String[maxLogLines][];
    private static int nextLine = 0;
    private static int numLogs = 0;

    /**
     * Set maximum number of lines to log. Must be power of 2.
     * If more than n lines are logged older logs will be lost.
     *
     * @param n maximum lines in the logging buffer
     */
    public static void setMaxLogLines(int n) {

        maxLogLines = n;
        indexMask = n - 1;
        nextLine = 0;
        numLogs = 0;

        logLines = new String[maxLogLines][];
    }

    /**
     * Add a log to the circular buffer
     *
     * @param log string to add
     * @return void
     */
    public static void addLog(String log) {
        logLines[nextLine++] = new String[]{(new StringBuffer().append(Utils.w2x(numLogs++)).append(": ").append(log)).toString(), null};
        nextLine &= indexMask;
    }

    /**
     * Add a log pair to the circular buffer
     *
     * @param logFirst  string corresponding to first part of log pair
     * @param logSecond string corresponding to second part of log pair
     * @return void
     */
    public static void addLogPair(String logFirst, String logSecond) {
        logLines[nextLine++] = new String[]{logFirst, logSecond};
        nextLine &= indexMask;
    }

    /**
     * Update previous log pair in the circular buffer
     *
     * @param logFirst  string corresponding to first part of log pair
     * @param logSecond string corresponding to second part of log pair
     * @return void
     */
    public static void updateLogPair(String logFirst, String logSecond) {
        nextLine = (--nextLine) & indexMask;
        logLines[nextLine++] = new String[]{logFirst, logSecond};
        nextLine &= indexMask;
    }

    /**
     * Add a "title" log to the circular buffer. The title log is not prefixed with
     * a log number
     *
     * @param title string to add
     * @return void
     */
    public static void addTitleLog(String title) {
        logLines[nextLine++] = new String[]{title, null};
        nextLine &= indexMask;
    }

    /**
     * Dump the entire contents of the buffer
     *
     * @param buffer     the buffer to dump
     * @param lineLength maximum log line length
     * @param sep        true add ' ' between octets false no ' '
     * @param prefix     true prefix log line with log number false no prefix
     * @return the first line of logging
     */
    public static String dump(byte[] buffer, int lineLength, boolean sep, boolean prefix) {

        int offset = 0;
        int bufLen;
        String first = null;
        String last;

        if (null == buffer) {
            first = "<null>";
            Utils.addLog(first);
        } else {
            for (bufLen = buffer.length; bufLen >= lineLength; bufLen -= lineLength, offset += lineLength) {
                if (sep) last = Utils.a2x(buffer, offset, lineLength, ' ');
                else last = Utils.a2x(buffer, offset, lineLength);
                if (null == first) first = last;
                if (prefix) Utils.addLog(last);
                else addTitleLog(last);
            }
            if (bufLen > 0) {
                if (sep) last = Utils.a2x(buffer, offset, bufLen, ' ');
                else last = Utils.a2x(buffer, offset, bufLen);
                if (null == first) first = last;
                if (prefix) Utils.addLog(last);
                else addTitleLog(last);
            }
        }

        return first;
    }

    /**
     * Clear the circular logging buffer
     *
     * @return void
     */
    public static void clearLogs() {
        logLines = new String[maxLogLines][];
        nextLine = 0;
        numLogs = 0;
    }

    /**
     * Get all logs presently in the buffer for the given part.
     * Allows a separator to be specified to be appended to the log.
     * Each log is terminated with a newline '\n'.
     *
     * @return String all of the logs
     */
    public static String getLogPart(int part, String sep) {

        StringBuffer logs = new StringBuffer("");

        int currLine = nextLine;
        do {
            String[] line = logLines[currLine++];
            currLine &= indexMask;

            if (null != line) {
                String log = line[part];
                if (!log.isEmpty()) {
                    logs = logs.append(log).append(sep);
                }
                logs = logs.append('\n');
            }

        } while (currLine != nextLine);

        return logs.toString();
    }

    /**
     * Get the length of the longest log presently in the buffer
     * for the given part. Useful for formatting multi-column
     * output in e.g. logcat.
     *
     * @return String all of the logs
     */
    public static int getMaxLogPartLength(int part) {

        int maxLogLen = 0;
        int currLine = nextLine;
        do {
            String[] line = logLines[currLine++];
            currLine &= indexMask;

            if (null != line) {
                String log = line[part];
                if (!log.isEmpty()) {
                    int logLen = log.length();
                    if (logLen > maxLogLen) {
                        maxLogLen = logLen;
                    }
                }
            }

        } while (currLine != nextLine);

        return maxLogLen;
    }

    /**
     * Get all logs presently in the buffer for the given part.
     * Each log is terminated with a newline '\n'.
     *
     * @return String all of the logs
     */
    public static String getLogPart(int part) {
        return getLogPart(part, "");
    }

    /**
     * Get all logs presently in the buffer. Each log is
     * terminated with a newline '\n'.
     *
     * @return String all of the logs
     */
    public static String getLogs() {
        return getLogPart(0);
    }

    /**
     * Get all logs presently in the buffer. Each log is
     * terminated with a newline '\n'. Each log is written
     * to the Android logcat
     *
     * @param tag tag to emit in logcat
     * @return String all of the logs
     */
    public static String toLogcat(String tag) {

        StringBuffer logs = new StringBuffer("");

        int currLine = nextLine;
        do {
            String[] line = logLines[currLine++];
            currLine &= indexMask;
            if (null != line) {
                String log = line[0];
                logs = logs.append(log).append('\n');
                //Log.i(tag, log);
            }
        } while (currLine != nextLine);

        return logs.toString();
    }

    /**
     * Get all logs presently in the buffer. Each log is
     * terminated with a newline '\n'. Each log is written
     * to the Android logcat
     *
     * @param tag tag to emit in logcat
     * @return String all of the logs
     */
    public static String logPairsToLogcat(String tag) {

        StringBuffer logs = new StringBuffer("");

        int maxLogPartLen = getMaxLogPartLength(0);
        String spaces = "                                             ";
        int spacesLen = spaces.length();
        maxLogPartLen = (maxLogPartLen > spacesLen ? spacesLen : maxLogPartLen);

        int currLine = nextLine;
        do {
            String[] line = logLines[currLine++];
            currLine &= indexMask;
            if (null != line) {
                String logFirst = line[0];
                int logLen = logFirst.length();
                String logSecond = line[1];
                String log = (new StringBuffer().append(logFirst).append(logLen == 0 ? "" : ":").append(spaces.substring(0, maxLogPartLen - logLen + 1 + (logLen == 0 ? 1 : 0))).append(logSecond)).toString();
                logs = logs.append(log).append('\n');
                //Log.i(tag, log);
            }
        } while (currLine != nextLine);

        return logs.toString();
    }

    /**
     * Convert a single int to its hex equivalent
     *
     * @param n integer to convert
     * @return char representing the hex value of the int passed in
     */
    static char n2x(int n) {
        char[] x = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f'};

        n &= 0xf;
        return x[n];
    }

    /**
     * Append (or fill if empty) the stringbuffer passed in with the
     * hex equivalent of the long passed in
     *
     * @param sb  stringbuffer to convert
     * @param dec long int to convert
     * @return StringBuffer of hexed values
     */
    static StringBuffer b2x(StringBuffer sb, long dec) {
        int d = (int) (dec);
        return sb.append(n2x(d >> 4)).append(n2x(d));
    }

    /**
     * Return a String containing the hex equivalent of the integer passed in
     *
     * @param dec integer to convert
     * @return String representation of the string buffer containing the hex
     */
    static String b2x(int dec) {
        return b2x(new StringBuffer(), dec).toString();
    }

    /**
     * Return a String containing the hex equivalent of the byte array passed in
     *
     * @param a byte array of the input data
     * @param o offset into the byte array to convert
     * @param l Length in bytes to convert
     * @return String containing the hex output
     */
    static String a2x(byte[] a, int o, int l) {
        StringBuffer sb = new StringBuffer();
        for (int i = 0; i < l; i++) {
            b2x(sb, a[o + i]);
        }
        return sb.toString();
    }

    /**
     * Return a String with desired separation
     * containing the hex equivalent of the byte array passed in
     *
     * @param a   byte array of the input data
     * @param o   offset into the byte array to convert
     * @param l   Length in bytes to convert
     * @param sep Add a separator to the output
     * @return String containing the hex output
     */
    static String a2x(byte[] a, int o, int l, char sep) {
        StringBuffer sb = new StringBuffer();
        for (int i = 0; i < l; i++) {
            if (i > 0) sb.append(sep);
            b2x(sb, a[o + i]);
        }
        return sb.toString();
    }

    static String w2x(int dec) {
        return b2x(b2x(new StringBuffer(), dec >> 8), dec).toString();
    }

    static String w2x(int dec, char sep) {
        return b2x(b2x(new StringBuffer(), dec >> 8).append(sep), dec).append(sep).toString();
    }

    static String i2x(int dec) {
        return b2x(b2x(b2x(b2x(new StringBuffer(), dec >> 24), dec >> 16), dec >> 8), dec).toString();
    }

    static String i2x(int dec, char sep) {
        return b2x(b2x(b2x(b2x(new StringBuffer(), dec >> 24).append(sep), dec >> 16).append(sep), dec >> 8).append(sep), dec).append(sep).toString();
    }

    static String l2x(long dec) {
        return b2x(b2x(b2x(b2x(b2x(b2x(b2x(b2x(new StringBuffer(), dec >> 56), dec >> 48), dec >> 40), dec >> 32), dec >> 24), dec >> 16), dec >> 8), dec).toString();
    }

    static String l2x(long dec, char sep) {
        return b2x(b2x(b2x(b2x(b2x(b2x(b2x(b2x(new StringBuffer(), dec >> 56).append(sep), dec >> 48).append(sep), dec >> 40).append(sep), dec >> 32).append(sep), dec >> 24).append(sep), dec >> 16).append(sep), dec >> 8).append(sep), dec).append(sep).toString();
    }


    /**
     * Provide byte array containing the un-hexed equivalent of
     * the hex string passed in
     *
     * @param s Hex string
     * @return byte array representation of string passed in
     */
    public static byte[] x2a(String s) {
        byte[] b = new byte[s.length() / 2];
        for (int i = 0; i < b.length; i++) {
            int index = i * 2;
            int v = Integer.parseInt(s.substring(index, index + 2), 16);
            b[i] = (byte) v;
        }
        return b;
    }


    static String exceptionToString(Throwable ex) {
        StringBuilder out = new StringBuilder();

        boolean first = true;
        while (ex != null) {
            if (first) {
                out.append("Exception:\n");
                first = false;
            } else {
                out.append("caused by:\n");
            }

            out.append(ex);
            out.append("\n");

            ex = ex.getCause();
        }

        return out.toString();
    }

}
