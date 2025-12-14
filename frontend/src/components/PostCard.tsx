import './PostCard.css'
import { type Post, getTimeAgo, getInitials, getCategoryIcon } from '../data/mockData'

interface PostCardProps {
    post: Post
    onClick?: () => void
}

export default function PostCard({ post, onClick }: PostCardProps) {
    if (!post) return null;
    return (
        <div className="post-card glass" onClick={onClick}>
            <div className="post-votes">
                <button className="vote-btn upvote" onClick={(e) => e.stopPropagation()}>
                    <span>▲</span>
                </button>
                <span className={`vote-count ${post.upvotes_count > 0 ? 'positive' : ''}`}>
                    {post.upvotes_count}
                </span>
                <button className="vote-btn downvote" onClick={(e) => e.stopPropagation()}>
                    <span>▼</span>
                </button>
            </div>

            <div className="post-content">
                <div className="post-header">
                    <div className="post-meta">
                        {post.category && (
                            <span className="category-badge badge">
                                {getCategoryIcon(post.category.slug)} {post.category.name}
                            </span>
                        )}
                        <div className="author-info">
                            <div className="author-avatar-small">
                                {getInitials(post.author?.first_name || post.author?.email, post.author?.last_name)}
                            </div>
                            <span className="post-author">
                                {post.author?.first_name ? `${post.author.first_name} ${post.author.last_name}` : post.author?.email}
                                {post.author?.role !== 'user' && (
                                    <span className={`role-tag ${post.author?.role}`}>
                                        {post.author?.role}
                                    </span>
                                )}
                            </span>
                        </div>
                        <span className="post-time">{getTimeAgo(post.created_at)}</span>
                    </div>
                </div>

                <div className="post-badges">
                    {post.is_pinned && <span className="pin-badge">📌 Pinned</span>}
                    {post.is_locked && <span className="lock-badge">🔒 Locked</span>}
                </div>

                <h3 className="post-title">{post.title}</h3>
                <p className="post-text">
                    {(post.content || '').length > 200
                        ? (post.content || '').substring(0, 200) + '...'
                        : (post.content || '')}
                </p>

                <div className="post-footer">
                    <button className="post-action" onClick={(e) => e.stopPropagation()}>
                        <span className="action-icon">💬</span>
                        <span>{post.comments_count} Comments</span>
                    </button>

                </div>
            </div>
        </div>
    )
}
