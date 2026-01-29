package app.rettiwtSpring.config;

import java.util.Map;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
public class GlobalExceptionHandler {
    
    @ExceptionHandler(UserNotFoundException.class)
    public ResponseEntity<Map<String, String>> handleUserNotFound(UserNotFoundException ex) {
        return createResponse(ex.getMessage(), HttpStatus.NOT_FOUND);
    }

    @ExceptionHandler(PostNotFoundException.class)
    public ResponseEntity<Map<String, String>> handlePostNotFound(PostNotFoundException ex) {
        return createResponse(ex.getMessage(), HttpStatus.NOT_FOUND);
    }

    @ExceptionHandler(InvalidPasswordException.class)
    public ResponseEntity<Map<String, String>> handleInvalidPassword(InvalidPasswordException ex) {
        return createResponse(ex.getMessage(), HttpStatus.UNAUTHORIZED);
    }

    @ExceptionHandler(RuntimeException.class)
    public ResponseEntity<Map<String, String>> handleRuntimeException(RuntimeException ex) {
        return createResponse(ex.getMessage(), HttpStatus.BAD_REQUEST);
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<Map<String, String>> handleValidation(MethodArgumentNotValidException ex) {
        String msg = ex.getBindingResult().getFieldErrors().get(0).getDefaultMessage();
        return createResponse(msg, HttpStatus.BAD_REQUEST);
    }

    private ResponseEntity<Map<String, String>> createResponse(String message, HttpStatus status) {
        return new ResponseEntity<>(Map.of("detail", message), status);
    }
}
