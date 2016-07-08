
public class TestMain {
    private static void usage() {
        System.out.println("use: TestMain c(client)/s(server)/sc(stdio-client)/ss(stdio-server)/tc/ts (Ip) \n" +
                "debug: dc/ds");
        System.exit(0);
    }

    public static void main(String[] args) throws Exception {
        if( args.length != 2 ) {
            usage();
        }
        String proPath = System.getProperty("user.dir");
        System.out.println(proPath);
        if( args[0].toLowerCase().equals("c") || args[0].toLowerCase().equals("cilent") ){
            TestClient client = new TestClient(args[1].toString(), 4001);
            client.init();
        } else if( args[0].toLowerCase().equals("s") || args[0].toLowerCase().equals("server") ) {
            TestServer server = new TestServer(args[1].toString(), 4001);
            server.init();
        } else if( args[0].toLowerCase().equals("sc") || args[0].toLowerCase().equals("stdio-client") ) {
            TestStdioClient client = new TestStdioClient(args[1].toString(), 4001);
            client.init();
        } else if( args[0].toLowerCase().equals("ss") || args[0].toLowerCase().equals("stdio-server") ) {
            TestStdioServer server = new TestStdioServer(args[1].toString(), 4001);
            server.init();
        } else if( args[0].toLowerCase().equals("tc") ) {
            TestThreadClient client = new TestThreadClient(args[1].toString(), 4001);
            client.init();
        } else if( args[0].toLowerCase().equals("ts") ) {
            TestThreadServer server = new TestThreadServer(args[1].toString(), 4001);
            server.init();
        } else if( args[0].toLowerCase().equals("dc") ) {
            TestPackageClient client = new TestPackageClient(args[1].toString(), 4001);
            client.init();
        } else if( args[0].toLowerCase().equals("ds") ) {
            TestPackageServer server = new TestPackageServer(args[1].toString(), 4001);
            server.init();
        } else {
            usage();
        }
    }
}
