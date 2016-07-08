import java.net.StandardSocketOptions;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.net.InetSocketAddress;
import java.net.ServerSocket;
import java.nio.ByteBuffer;
import java.nio.channels.SelectionKey;
import java.nio.channels.Selector;
import java.nio.channels.ServerSocketChannel;
import java.nio.channels.SocketChannel;
import java.util.Iterator;
import java.util.Set;



public class TestPackageServer {
    private int port = 8001;
    private String ipAddress = "0.0.0.0";
    private Selector selector;
    private final int BLOCK = 204800;
    private ByteBuffer readBuffer;
    private ByteBuffer writeBuffer;
    private String textSend;

    public TestPackageServer(String address, int port) throws IOException {
        this.port = port;
        this.ipAddress = address;
        readBuffer = ByteBuffer.allocate(this.BLOCK);
        writeBuffer = ByteBuffer.allocate(this.BLOCK);
    }

    public void init() throws IOException {
        ServerSocketChannel serverChannel = ServerSocketChannel.open();
        serverChannel.configureBlocking(false);

        ServerSocket serverSocket = serverChannel.socket();
        serverSocket.bind(new InetSocketAddress(this.ipAddress, this.port));

        this.selector = Selector.open();
        serverChannel.register(selector, SelectionKey.OP_ACCEPT);

        readFile();
        listenConnect();
    }

    private void listenConnect() throws IOException {
        ServerSocketChannel serverSocketChannel = null;
        SocketChannel socketChannel = null;

        while(true) {
            this.selector.select();
            Set selectorKeys = this.selector.selectedKeys();
            Iterator iterator = selectorKeys.iterator();
            int count = 0;

            while(iterator.hasNext()) {
                SelectionKey key = (SelectionKey) iterator.next();

                if(key.isAcceptable()) {
                    serverSocketChannel = (ServerSocketChannel)key.channel();
                    socketChannel = serverSocketChannel.accept();
                    socketChannel.configureBlocking(false);
                    socketChannel.register(this.selector, SelectionKey.OP_READ);
                    System.out.println("get new connection: " + socketChannel.getRemoteAddress().toString());
                } else if(key.isReadable()) {
                    socketChannel = (SocketChannel)key.channel();
                    System.out.println("buffer size: " + socketChannel.getOption(StandardSocketOptions.SO_RCVBUF));
                    count = socketChannel.read(readBuffer);
                    String strBuffer;
                    if(count > 0) {
                        strBuffer = new String(readBuffer.array(), 0, count);
                        //System.out.println("count: " + count);
                        System.out.println(strBuffer.getBytes().length);
                        //System.out.println(strBuffer);
                        //System.out.println("received " + count + "\n" + strBuffer.toString());

                    }
                    readBuffer.clear();
                    //socketChannel.register(this.selector, SelectionKey.OP_WRITE);
                } else if(key.isWritable()) {
                    writeBuffer.clear();
                    socketChannel = (SocketChannel)key.channel();
                    String text = this.textSend.substring(0, 2046);
                    writeBuffer.put(text.getBytes());
                    writeBuffer.flip();
                    socketChannel.write(writeBuffer);
                    //socketChannel.register(this.selector, SelectionKey.OP_READ);
                } else {
                    System.out.println("what's wrong");
                }
                iterator.remove();
            }

        }
    }

    private void readFile() throws IOException {
        String proPath = getProjectPath();
        System.out.println(proPath);
        String fileName = proPath + "/doc/1.txt";
        File file = new File(fileName);
        BufferedReader reader = new BufferedReader(new FileReader(file));

        String line = null;
        while ( (line = reader.readLine()) != null ) {
            this.textSend += line;
        }
        reader.close();
    }

    private String getProjectPath() throws IOException {
        return System.getProperty("user.dir");
    }

}
