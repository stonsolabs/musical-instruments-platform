'use client';

import React, { useState, useEffect } from 'react';
import { apiClient } from '@/lib/api';

interface VoteStats {
  thumbs_up_count: number;
  thumbs_down_count: number;
  total_votes: number;
  vote_score: number;
  user_vote?: 'up' | 'down' | null;
}

interface ProductVotingProps {
  productId: number;
  initialStats?: VoteStats;
  className?: string;
  size?: 'small' | 'medium' | 'large';
  showNumbers?: boolean;
}

export default function ProductVoting({ 
  productId, 
  initialStats,
  className = '',
  size = 'medium',
  showNumbers = true
}: ProductVotingProps) {
  const [voteStats, setVoteStats] = useState<VoteStats | null>(initialStats || null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Size variants
  const sizeClasses = {
    small: {
      container: 'gap-1',
      button: 'w-8 h-8 text-sm',
      text: 'text-xs',
      icon: 'text-sm'
    },
    medium: {
      container: 'gap-2',
      button: 'w-10 h-10 text-base',
      text: 'text-sm',
      icon: 'text-base'
    },
    large: {
      container: 'gap-3',
      button: 'w-12 h-12 text-lg',
      text: 'text-base',
      icon: 'text-lg'
    }
  };

  const classes = sizeClasses[size];

  // Load vote stats on mount if not provided
  useEffect(() => {
    if (!initialStats) {
      loadVoteStats();
    }
  }, [productId, initialStats]);

  const loadVoteStats = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const stats = await apiClient.getProductVoteStats(productId);
      setVoteStats(stats);
    } catch (err) {
      console.error('Failed to load vote stats:', err);
      setError('Failed to load voting data');
    } finally {
      setIsLoading(false);
    }
  };

  const handleVote = async (voteType: 'up' | 'down') => {
    if (isLoading) return;

    try {
      setIsLoading(true);
      setError(null);
      
      const response = await apiClient.voteOnProduct(productId, voteType);
      
      if (response.success) {
        // Update vote stats based on response
        setVoteStats({
          thumbs_up_count: response.vote_counts.thumbs_up,
          thumbs_down_count: response.vote_counts.thumbs_down,
          total_votes: response.vote_counts.total,
          vote_score: response.vote_counts.score,
          user_vote: response.user_vote
        });
      }
    } catch (err) {
      console.error('Failed to vote:', err);
      setError('Failed to record vote');
      // Reload stats to get current state
      loadVoteStats();
    } finally {
      setIsLoading(false);
    }
  };

  if (error && !voteStats) {
    return (
      <div className={`text-red-500 ${classes.text} ${className}`}>
        Unable to load voting
      </div>
    );
  }

  if (!voteStats) {
    return (
      <div className={`flex items-center ${classes.container} ${className}`}>
        <div className={`animate-pulse bg-gray-200 rounded-full ${classes.button}`}></div>
        <div className="animate-pulse bg-gray-200 h-4 w-8 rounded"></div>
        <div className={`animate-pulse bg-gray-200 rounded-full ${classes.button}`}></div>
      </div>
    );
  }

  return (
    <div className={`flex items-center ${classes.container} ${className}`}>
      {/* Thumbs Up Button */}
      <button
        onClick={() => handleVote('up')}
        disabled={isLoading}
        className={`
          ${classes.button} rounded-full border-2 transition-all duration-200 
          ${voteStats.user_vote === 'up' 
            ? 'bg-green-500 border-green-500 text-white' 
            : 'bg-white border-gray-300 text-gray-600 hover:border-green-500 hover:text-green-500'
          }
          ${isLoading ? 'opacity-50 cursor-not-allowed' : 'hover:scale-105 active:scale-95'}
          flex items-center justify-center shadow-sm hover:shadow-md
        `}
        title={voteStats.user_vote === 'up' ? 'Remove thumbs up' : 'Thumbs up'}
      >
        <span className={classes.icon}>👍</span>
      </button>

      {/* Vote Display */}
      {showNumbers && (
        <div className="flex items-center gap-1">
          <span className={`font-semibold text-green-600 ${classes.text}`}>
            {voteStats.thumbs_up_count || 0}
          </span>
          <span className={`text-gray-400 ${classes.text}`}>|</span>
          <span className={`font-semibold text-red-600 ${classes.text}`}>
            {voteStats.thumbs_down_count || 0}
          </span>
        </div>
      )}

      {/* Vote Score (optional, for compact display) */}
      {!showNumbers && (
        <span className={`font-semibold ${classes.text} ${
          (voteStats.vote_score || 0) > 0 ? 'text-green-600' : 
          (voteStats.vote_score || 0) < 0 ? 'text-red-600' : 'text-gray-500'
        }`}>
          {(voteStats.vote_score || 0) > 0 ? '+' : ''}{voteStats.vote_score || 0}
        </span>
      )}

      {/* Thumbs Down Button */}
      <button
        onClick={() => handleVote('down')}
        disabled={isLoading}
        className={`
          ${classes.button} rounded-full border-2 transition-all duration-200 
          ${voteStats.user_vote === 'down' 
            ? 'bg-red-500 border-red-500 text-white' 
            : 'bg-white border-gray-300 text-gray-600 hover:border-red-500 hover:text-red-500'
          }
          ${isLoading ? 'opacity-50 cursor-not-allowed' : 'hover:scale-105 active:scale-95'}
          flex items-center justify-center shadow-sm hover:shadow-md
        `}
        title={voteStats.user_vote === 'down' ? 'Remove thumbs down' : 'Thumbs down'}
      >
        <span className={classes.icon}>👎</span>
      </button>

      {/* Error Message */}
      {error && (
        <span className={`text-red-500 ${classes.text} ml-2`}>
          {error}
        </span>
      )}
    </div>
  );
}

// Compact voting component for product cards
export function CompactProductVoting({ productId, initialStats, className = '' }: Pick<ProductVotingProps, 'productId' | 'initialStats' | 'className'>) {
  return (
    <ProductVoting 
      productId={productId}
      initialStats={initialStats}
      size="small"
      showNumbers={false}
      className={className}
    />
  );
}

// Full voting component for product detail pages
export function DetailedProductVoting({ productId, initialStats, className = '' }: Pick<ProductVotingProps, 'productId' | 'initialStats' | 'className'>) {
  return (
    <div className={`bg-gray-50 rounded-lg p-4 ${className}`}>
      <div className="text-center mb-3">
        <h3 className="text-sm font-medium text-gray-700 mb-1">Rate this product</h3>
        <p className="text-xs text-gray-500">Help other musicians with your opinion</p>
      </div>
      <ProductVoting 
        productId={productId}
        initialStats={initialStats}
        size="large"
        showNumbers={true}
        className="justify-center"
      />
      {initialStats && initialStats.total_votes > 0 && (
        <div className="text-center mt-3">
          <p className="text-xs text-gray-500">
            {initialStats.total_votes} {initialStats.total_votes === 1 ? 'vote' : 'votes'} total
          </p>
        </div>
      )}
    </div>
  );
}
