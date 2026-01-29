package app.rettiwtSpring.dto;

import org.hibernate.validator.constraints.Length;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class LoginRequest {
    @NotBlank(message="Your username or email are missing")
    @Size(min = 3, max = 24, message="Username or email must have between 3 and 24 characters")
    private String username_or_email;
    @NotBlank(message="Password cannot be blank")
    @Size(min = 3, message="Password must have at least 3 characters")
    private String password;
}
