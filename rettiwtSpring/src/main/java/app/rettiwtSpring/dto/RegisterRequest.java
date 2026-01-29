package app.rettiwtSpring.dto;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class RegisterRequest {
    @NotBlank(message="Username cannot be blank")
    @Size(min = 3, max = 24, message="Username must have between 3 and 24 characters")
    private String username;
    @Email(message="Wrong email format")
    @NotBlank(message= "Email cannot be blank")
    private String email;
    @NotBlank
    @Size(min = 3, message="Password must have at least 3 characters")
    private String password;
}
