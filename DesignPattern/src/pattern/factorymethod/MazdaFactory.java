package pattern.factorymethod;

/**
 * Created by Yan on 8/30/2016.
 */
// mazda factory to produce mazda cars
public class MazdaFactory implements Factories {
    @Override
    public Cars produce() {
        return new Mazda();
    }
}
