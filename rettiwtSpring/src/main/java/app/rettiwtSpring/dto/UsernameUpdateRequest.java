package app.rettiwtSpring.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class UsernameUpdateRequest {
    @NotBlank(message="Username is required")
    @Size(min = 3, max = 24, message="Username must have between 3 and 24 characters")
    private String new_username;
}
