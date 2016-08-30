package pattern.factorymethod;

/**
 * Created by Yan on 8/30/2016.
 */
// one bmw car product
public class Bmw implements Cars {
    @Override
    public void printStyle() {
        System.out.println("It's BMW style");
    }
}
