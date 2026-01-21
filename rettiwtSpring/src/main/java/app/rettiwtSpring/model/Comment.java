package app.rettiwtSpring.model;

import java.time.Instant;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.PrePersist;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Entity
@Table(name="comments")
@Getter @Setter
@AllArgsConstructor @NoArgsConstructor
public class Comment {
    @Id
    @GeneratedValue(strategy=GenerationType.IDENTITY)
    private Long id;
    @Column(columnDefinition="TEXT", nullable=false)
    private String text;
    @ManyToOne(optional=false, fetch=FetchType.LAZY)
    @JoinColumn(name="id_post")
    private Post post;
    @ManyToOne(optional=false, fetch=FetchType.LAZY)
    @JoinColumn(name="id_user")
    private User user;
    @Column(name="created_at", updatable=false)
    private Instant createdAt;
    
    @PrePersist
    protected void onCreate(){
        createdAt = Instant.now();
    }
}
