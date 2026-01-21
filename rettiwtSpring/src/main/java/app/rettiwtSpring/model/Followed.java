package app.rettiwtSpring.model;

import java.time.Instant;

import jakarta.persistence.Column;
import jakarta.persistence.EmbeddedId;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.MapsId;
import jakarta.persistence.PrePersist;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Entity
@Table(name="followed")
@Getter @Setter
@NoArgsConstructor @AllArgsConstructor
public class Followed {
    @EmbeddedId
    private FollowedId id;
    @ManyToOne(fetch = FetchType.LAZY)
    @MapsId("idUser")
    @JoinColumn(name="id_user")
    private User user;
    @ManyToOne(fetch = FetchType.LAZY)
    @MapsId("byUser")
    @JoinColumn(name="by_user")
    private User followedBy;
    @Column(name="created_at", updatable=false)
    private Instant createdAt;
    
    @PrePersist
    protected void onCreate(){
        createdAt = Instant.now();
    }
}
