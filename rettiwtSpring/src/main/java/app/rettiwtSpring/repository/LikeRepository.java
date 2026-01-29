package app.rettiwtSpring.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import app.rettiwtSpring.model.Like;
import app.rettiwtSpring.model.LikeId;
import jakarta.transaction.Transactional;

@Repository
public interface LikeRepository extends JpaRepository<Like, LikeId>{
    @Query("SELECT l FROM Like l WHERE l.post.id = :postId")
    List<Like> findByPostIdPost(Long postId);

    @Query("SELECT COUNT(1) > 0 FROM Like l WHERE l.post.id = :postId AND l.user.id = :userId")
    boolean existsByPostIdAndUserId(Long postId, Long userId);

    @Query("SELECT COUNT(l) FROM Like l WHERE l.post.id = :postId")
    int countByPostId(Long postId);

    @Query("DELETE FROM Like l WHERE l.post.id = :postId AND l.user.id = :userId")
    @Modifying
    @Transactional
    void deleteByPostIdAndUserId(Long postId, Long userId);

}
