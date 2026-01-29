package app.rettiwtSpring.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import app.rettiwtSpring.model.Followed;
import app.rettiwtSpring.model.FollowedId;
import app.rettiwtSpring.model.User;
import jakarta.transaction.Transactional;


@Repository
public interface FollowedRepository extends JpaRepository<Followed, FollowedId> {
    List<Followed> findByUser(User user);
    
    List<Followed> findByFollowedBy(User followedBy);

    boolean existsByUserAndFollowedBy(User user, User followedBy);

    @Modifying
    @Transactional
    @Query("DELETE FROM Followed f WHERE f.user = :user AND f.followedBy = :byUser")
    void deleteByUserAndFollowedBy(User user, User byUser);
}
