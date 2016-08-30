package pattern.factorymethod;

/**
 * Created by Yan on 8/30/2016.
 */
// one mazda car product
public class Mazda implements Cars {
    @Override
    public void printStyle() {
        System.out.println("It's Mazda style");
    }
}
