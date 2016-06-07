import java.io.IOException;

public class TestMain {
	
	public static void main(String [] args) throws IOException {
		
	    test_client();	
		return;
	}
	
	public static void test_server() throws IOException {
		TestNioServer server = new TestNioServer();
		server.m_iPort = 2000;
		server.init_server();
		server.listen_server();
		return;
	}

	public static void test_client() throws IOException {
		TestNioClient client = new TestNioClient();
		client.m_iPort = 2001;
		client.m_strIpAddress = "192.168.56.101";
		client.init_client();
		client.listen_client();
		return;
	}
}
