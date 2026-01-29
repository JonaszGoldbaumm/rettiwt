package app.rettiwtSpring.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class PasswordUpdateRequest {
    @NotBlank
    @Size(min = 3, message="Password must have at least 3 characters")
    private String new_password;
    @NotBlank
    @Size(min = 3, message="Password must have at least 3 characters")
    private String old_password;
}

