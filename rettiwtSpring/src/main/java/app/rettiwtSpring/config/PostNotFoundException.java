package app.rettiwtSpring.config;

public class PostNotFoundException extends RuntimeException {

    public PostNotFoundException(String message) {
        super("Post not found: " + message);
    }
    
}
