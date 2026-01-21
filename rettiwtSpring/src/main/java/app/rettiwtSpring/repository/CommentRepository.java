package app.rettiwtSpring.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import app.rettiwtSpring.model.Comment;
import app.rettiwtSpring.model.Post;


@Repository
public interface CommentRepository extends JpaRepository<Comment, Long>{
    List<Comment> findByPostOrderByCreatedAtAsc(Post post);
}
