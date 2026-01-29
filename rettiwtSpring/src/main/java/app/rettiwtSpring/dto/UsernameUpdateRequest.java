package app.rettiwtSpring.dto;

import jakarta.validation.constraints.NotBlank;
import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class UsernameUpdateRequest {
    @NotBlank
    private String new_username;
}
