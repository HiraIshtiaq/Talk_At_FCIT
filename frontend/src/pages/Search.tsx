import { useState, useEffect } from 'react';
import { type Post, type User, type Category, getTimeAgo, getInitials, getCategoryIcon } from '../data/mockData';
import { discussions } from '../services/api';
import './Search.css';

interface SearchProps {
    onNavigate: (page: string) => void;
    onViewPost: (post: Post) => void;
}

type SearchTab = 'posts' | 'users' | 'categories';

const Search = ({ onNavigate: _onNavigate, onViewPost }: SearchProps) => {
    const [query, setQuery] = useState('');
    const [activeTab, setActiveTab] = useState<SearchTab>('posts');
    const [searchResults, setSearchResults] = useState<{
        posts: Post[];
        users: User[];
        categories: Category[];
    }>({
        posts: [],
        users: [],
        categories: []
    });
    const [hasSearched, setHasSearched] = useState(false);
    const [loading, setLoading] = useState(false);
    const [initialCategories, setInitialCategories] = useState<Category[]>([]);

    useEffect(() => {
        discussions.getCategories()
            .then(res => {
                const results = Array.isArray(res.data) ? res.data : (res.data as any).results || [];
                setInitialCategories(results);
            })
            .catch(err => console.error("Failed to fetch initial categories", err));
    }, []);

    const handleSearch = async (searchQuery: string) => {
        setQuery(searchQuery);

        if (searchQuery.trim().length < 2) {
            setSearchResults({ posts: [], users: [], categories: [] });
            setHasSearched(false);
            return;
        }

        setLoading(true);
        try {
            // Only searching posts and categories for now
            const [postsRes, catsRes] = await Promise.all([
                discussions.getPosts(undefined, searchQuery),
                discussions.getCategories() // Search not supported? Fetch all and filter
            ]);

            const posts = Array.isArray(postsRes.data) ? postsRes.data : (postsRes.data as any).results || [];
            // If backend supports search on categories, use it. But for now filter all.
            // Actually getCategories doesn't take params in my api definition?
            // api.ts: getCategories: () => api.get<Category[]>('/discussions/categories/')
            // So we fetch all.
            const allCats = Array.isArray(catsRes.data) ? catsRes.data : (catsRes.data as any).results || [];

            const filteredCats = allCats.filter((c: any) => c.name.toLowerCase().includes(searchQuery.toLowerCase()));

            setSearchResults({
                posts: posts,
                users: [],
                categories: filteredCats
            });
            setHasSearched(true);
        } catch (error) {
            console.error("Search failed", error);
        } finally {
            setLoading(false);
        }
    };

    const totalResults =
        searchResults.posts.length +
        searchResults.users.length +
        searchResults.categories.length;

    const getTabCount = (tab: SearchTab): number => {
        switch (tab) {
            case 'posts': return searchResults.posts.length;
            case 'users': return searchResults.users.length;
            case 'categories': return searchResults.categories.length;
        }
    };

    return (
        <div className="search-page fade-in">
            <div className="search-header">
                <h1>Search</h1>
                <p>Find posts, users, and categories</p>
            </div>

            <div className="search-box glass">
                <span className="search-icon">🔍</span>
                <input
                    type="text"
                    value={query}
                    onChange={(e) => handleSearch(e.target.value)}
                    placeholder="Search for anything..."
                    autoFocus
                    disabled={loading}
                />
                {query && !loading && (
                    <button className="clear-btn" onClick={() => handleSearch('')}>
                        ✕
                    </button>
                )}
                {loading && <span className="loading-spinner-small">...</span>}
            </div>

            {hasSearched && (
                <>
                    <div className="results-summary">
                        Found <strong>{totalResults}</strong> results for "{query}"
                    </div>

                    <div className="search-tabs">
                        {(['posts', 'users', 'categories'] as SearchTab[]).map(tab => (
                            <button
                                key={tab}
                                className={`search-tab ${activeTab === tab ? 'active' : ''}`}
                                onClick={() => setActiveTab(tab)}
                            >
                                {tab.charAt(0).toUpperCase() + tab.slice(1)}
                                {getTabCount(tab) > 0 && (
                                    <span className="tab-count">{getTabCount(tab)}</span>
                                )}
                            </button>
                        ))}
                    </div>

                    <div className="search-results">
                        {activeTab === 'posts' && (
                            <div className="posts-results">
                                {searchResults.posts.length > 0 ? (
                                    searchResults.posts.map(post => (
                                        <div
                                            key={post.id}
                                            className="result-card post-result"
                                            onClick={() => onViewPost(post)}
                                        >
                                            <div className="result-category">
                                                <span>{getCategoryIcon(post.category.slug)}</span>
                                                {post.category.name}
                                            </div>
                                            <h3 className="result-title">{post.title}</h3>
                                            <p className="result-excerpt">
                                                {post.content.substring(0, 150)}...
                                            </p>
                                            <div className="result-meta">
                                                <div className="result-author">
                                                    <div className="mini-avatar">
                                                        {getInitials(post.author.first_name, post.author.last_name)}
                                                    </div>
                                                    {post.author.first_name} {post.author.last_name}
                                                </div>
                                                <span className="result-stats">
                                                    ⬆️ {post.upvotes_count} • 💬 {post.comments_count}
                                                </span>
                                                <span className="result-time">{getTimeAgo(post.created_at)}</span>
                                            </div>
                                        </div>
                                    ))
                                ) : (
                                    <div className="no-results">
                                        <span className="no-results-icon">📝</span>
                                        <p>No posts found matching "{query}"</p>
                                    </div>
                                )}
                            </div>
                        )}

                        {activeTab === 'users' && (
                            <div className="users-results">
                                {searchResults.users.length > 0 ? (
                                    searchResults.users.map(user => (
                                        <div key={user.id} className="result-card user-result">
                                            <div className="user-avatar">
                                                {getInitials(user.first_name, user.last_name)}
                                            </div>
                                            <div className="user-info">
                                                <div className="user-name-row">
                                                    <h3>{user.first_name} {user.last_name}</h3>
                                                    {user.role !== 'user' && (
                                                        <span className={`role-tag ${user.role}`}>{user.role}</span>
                                                    )}
                                                    {user.is_verified && <span className="verified-tag">✓</span>}
                                                </div>
                                                <p className="user-email">{user.email}</p>
                                                <p className="user-bio">{user.bio}</p>
                                                <div className="user-stats">
                                                    <span>📝 {user.posts_count} posts</span>
                                                    <span>👥 {user.followers_count} followers</span>
                                                </div>
                                            </div>
                                            <button className="view-profile-btn">View Profile</button>
                                        </div>
                                    ))
                                ) : (
                                    <div className="no-results">
                                        <span className="no-results-icon">👤</span>
                                        <p>No users found matching "{query}"</p>
                                    </div>
                                )}
                            </div>
                        )}

                        {activeTab === 'categories' && (
                            <div className="categories-results">
                                {searchResults.categories.length > 0 ? (
                                    searchResults.categories.map(category => (
                                        <div key={category.id} className="result-card category-result">
                                            <div className="category-icon-large">
                                                {getCategoryIcon(category.slug)}
                                            </div>
                                            <div className="category-info">
                                                <h3>{category.name}</h3>
                                                <p>{category.description}</p>
                                                <span className="category-posts-count">
                                                    {category.posts_count} posts
                                                </span>
                                            </div>
                                            <button className="browse-category-btn">Browse</button>
                                        </div>
                                    ))
                                ) : (
                                    <div className="no-results">
                                        <span className="no-results-icon">📂</span>
                                        <p>No categories found matching "{query}"</p>
                                    </div>
                                )}
                            </div>
                        )}
                    </div>
                </>
            )}

            {!hasSearched && (
                <div className="search-suggestions">
                    <h3>Popular Categories</h3>
                    <div className="suggestion-chips">
                        {initialCategories.length > 0 ? initialCategories.slice(0, 5).map(category => (
                            <button
                                key={category.id}
                                className="suggestion-chip"
                                onClick={() => handleSearch(category.name)}
                            >
                                {getCategoryIcon(category.slug)} {category.name}
                            </button>
                        )) : <p>Loading categories...</p>}
                    </div>

                    <h3>Trending Topics</h3>
                    <div className="trending-list">
                        <button onClick={() => handleSearch('React')}>
                            🔥 React Development
                        </button>
                        <button onClick={() => handleSearch('Exam')}>
                            🔥 Exams
                        </button>
                        <button onClick={() => handleSearch('GSoC')}>
                            🔥 Google Summer of Code
                        </button>
                        <button onClick={() => handleSearch('Tech Fest')}>
                            🔥 Tech Fest 2024
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Search;
