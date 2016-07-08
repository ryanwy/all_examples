import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.nio.channels.SelectionKey;
import java.nio.channels.Selector;
import java.nio.channels.SocketChannel;
import java.util.Iterator;
import java.util.Random;
import java.util.Set;


public class TestPackageClient {
    private String serverIpAddress = "";
    private int port = 0;
    private Selector selector = null;
    private final int BLOCK = 2048;
    private ByteBuffer readBuffer = null;
    private ByteBuffer writeBuffer = null;
    private String textSend;

    public TestPackageClient(String serverIp, int port) {
        this.serverIpAddress = serverIp;
        this.port = port;
        this.readBuffer = ByteBuffer.allocate(BLOCK);
        this.writeBuffer = ByteBuffer.allocate(BLOCK);
    }

    public void init() throws IOException {
        SocketChannel socketChannel = SocketChannel.open();
        socketChannel.configureBlocking(false);

        this.selector = Selector.open();
        socketChannel.register(this.selector, SelectionKey.OP_CONNECT);
        socketChannel.connect(new InetSocketAddress(this.serverIpAddress, this.port));

        readFile();
        handleOperation();
    }

    private void handleOperation() throws IOException {
        SocketChannel socketChannel = null;

        while(true) {
            this.selector.select();
            Set selectorKeys = this.selector.selectedKeys();
            Iterator iterator = selectorKeys.iterator();
            int count = 0;

            while(iterator.hasNext()) {
                SelectionKey key = (SelectionKey)iterator.next();
                if(key.isConnectable()) {
                    socketChannel = (SocketChannel)key.channel();
                    if(socketChannel.isConnectionPending()) {
                        socketChannel.finishConnect();
                        writeBuffer.clear();
                        String message = "hello, this is client";
                        writeBuffer.put(message.getBytes());
                        writeBuffer.flip();
                        socketChannel.write(writeBuffer);
                    }
                    socketChannel.register(this.selector, SelectionKey.OP_WRITE);
                } else if(key.isReadable()) {
                    socketChannel = (SocketChannel)key.channel();
                    readBuffer.clear();
                    String strBuffer;
                    count = socketChannel.read(readBuffer);
                    if (count > 0) {
                        strBuffer = new String(readBuffer.array(), 0, count);
                        System.out.println("received " + count);
                    }

                    //socketChannel.register(this.selector, SelectionKey.OP_WRITE);
                } else if(key.isWritable()) {
                    writeBuffer.clear();
                    socketChannel = (SocketChannel) key.channel();
                    Random random = new Random();
                    int randomNum = random.nextInt(2048);
                    System.out.println("random: " + randomNum);
                    String text = this.textSend.substring(0, randomNum);
                    System.out.println(text.getBytes().length);
                    //System.out.println(text);
                    writeBuffer.put(text.getBytes());
                    writeBuffer.flip();
                    socketChannel.write(writeBuffer);
                    try {
                        Thread.sleep(2000);
                    } catch(InterruptedException e) {
                        e.printStackTrace();
                    }
                    //socketChannel.register(this.selector, SelectionKey.OP_READ);
                } else {
                    System.out.println("oh, anything wrong?");
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
