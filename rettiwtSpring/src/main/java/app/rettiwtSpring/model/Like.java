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
@Table(name="likes")
@Getter @Setter
@NoArgsConstructor @AllArgsConstructor
public class Like {

    @EmbeddedId
    private LikeId id;
    @ManyToOne(fetch=FetchType.LAZY)
    @MapsId("idPost")
    @JoinColumn(name="id_post")
    private Post post;
    @ManyToOne(fetch=FetchType.LAZY)
    @MapsId("idUser")
    @JoinColumn(name = "id_user")
    private User user;
    @Column(name= "created_at", updatable=false)
    private Instant createdAt;

    @PrePersist
    protected void onCreate(){
        createdAt = Instant.now();
    }
}