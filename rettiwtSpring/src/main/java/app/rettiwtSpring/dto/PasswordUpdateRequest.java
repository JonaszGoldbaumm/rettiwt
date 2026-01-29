package app.rettiwtSpring.dto;

import jakarta.validation.constraints.NotBlank;
import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class PasswordUpdateRequest {
    @NotBlank
    private String new_password;
    @NotBlank
    private String old_password;
}

