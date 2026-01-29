package app.rettiwtSpring.config;

public class InvalidPasswordException extends RuntimeException{

    public InvalidPasswordException(String arg0) {
        super(arg0 + "'s password is wrong!");
    }
    
}
