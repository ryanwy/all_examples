package pattern.factorymethod;

import jdk.nashorn.internal.ir.annotations.Ignore;

/**
 * Created by Yan on 8/30/2016.
 */
// bmw factory to produce bmw cars
public class BmwFactory implements Factories {
    @Override
    public Cars produce() {
        return new Bmw();
    }
}
