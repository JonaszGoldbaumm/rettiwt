package app.rettiwtSpring.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import app.rettiwtSpring.model.Post;
import app.rettiwtSpring.model.User;

@Repository
public interface PostRepository extends JpaRepository<Post, Long> {
    
    List<Post> findByUserOrderByCreatedAtDesc(User user);

    @Query("SELECT p FROM Post p ORDER BY p.createdAt DESC")
    List<Post> findAllPostsFeed();

    @Query("SELECT p FROM Post p JOIN FETCH p.user WHERE p.id = :id")
    Post findByIdWithUser(Long id);

    @Query("SELECT p FROM Post p JOIN FETCH p.user WHERE p.media IS NOT NULL ORDER BY p.createdAt DESC")
    List<Post> findPostsWithMedia();

    @Query("SELECT p FROM Post p JOIN FETCH p.user u WHERE u.id IN(SELECT f.user.id FROM Followed f WHERE f.followedBy.id = :userId) ORDER BY p.createdAt DESC")
    List<Post> findPostsFromFollowed(@Param("userId") Long userId);
}
