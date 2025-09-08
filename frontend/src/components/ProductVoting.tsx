import React, { useState } from 'react';
import { submitVote, getVoteStats } from '../lib/vote';
// Using emojis for vote icons per branding (🤘 for upvote)

interface ProductVotingProps {
  productId: number;
  initialUpvotes?: number;
  initialDownvotes?: number;
  userVote?: 'up' | 'down' | null;
  onVote?: (productId: number, vote: 'up' | 'down' | null) => void;
  disabled?: boolean;
}

export default function ProductVoting({
  productId,
  initialUpvotes = 0,
  initialDownvotes = 0,
  userVote = null,
  onVote,
  disabled = false
}: ProductVotingProps) {
  const [upvotes, setUpvotes] = useState(initialUpvotes);
  const [downvotes, setDownvotes] = useState(initialDownvotes);
  const [currentVote, setCurrentVote] = useState<'up' | 'down' | null>(userVote);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleVote = async (vote: 'up' | 'down') => {
    if (disabled || isSubmitting) return;

    setIsSubmitting(true);
    
    try {
      let newUpvotes = upvotes;
      let newDownvotes = downvotes;
      let newUserVote: 'up' | 'down' | null = vote;

      // Handle vote logic
      if (currentVote === vote) {
        // User is clicking the same vote - remove it
        if (vote === 'up') {
          newUpvotes = Math.max(0, upvotes - 1);
        } else {
          newDownvotes = Math.max(0, downvotes - 1);
        }
        newUserVote = null;
      } else if (currentVote === null) {
        // User is voting for the first time
        if (vote === 'up') {
          newUpvotes = upvotes + 1;
        } else {
          newDownvotes = downvotes + 1;
        }
      } else {
        // User is changing their vote
        if (currentVote === 'up') {
          newUpvotes = Math.max(0, upvotes - 1);
          newDownvotes = downvotes + 1;
        } else {
          newDownvotes = Math.max(0, downvotes - 1);
          newUpvotes = upvotes + 1;
        }
      }

      // Update local state
      setUpvotes(newUpvotes);
      setDownvotes(newDownvotes);
      setCurrentVote(newUserVote);

      // Call the onVote callback if provided
      if (onVote) {
        await onVote(productId, newUserVote);
      }

      // If no callback, make API call via proxy and then refetch stats
      if (!onVote) {
        await submitVote(productId, vote);
        const stats = await getVoteStats(productId);
        const up = Number(stats?.thumbs_up_count ?? 0);
        const down = Number(stats?.thumbs_down_count ?? 0);
        setUpvotes(up);
        setDownvotes(down);
        if (typeof stats?.user_vote === 'string' || stats?.user_vote === null) {
          setCurrentVote(stats.user_vote);
        }
      }
    } catch (error) {
      console.error('Error submitting vote:', error);
      // Revert local state on error
      setUpvotes(initialUpvotes);
      setDownvotes(initialDownvotes);
      setCurrentVote(userVote);
    } finally {
      setIsSubmitting(false);
    }
  };

  const totalVotes = upvotes + downvotes;
  const votePercentage = totalVotes > 0 ? Math.round((upvotes / totalVotes) * 100) : 0;

  return (
    <div className="flex flex-col items-center space-y-3 p-4 bg-gray-50 rounded-lg">
      <h4 className="text-sm font-medium text-gray-700">Was this helpful?</h4>
      
      <div className="flex items-center space-x-4">
        {/* Upvote Button */}
        <button
          onClick={() => handleVote('up')}
          disabled={disabled || isSubmitting}
          className={`flex items-center space-x-2 px-3 py-2 rounded-md transition-colors ${
            currentVote === 'up'
              ? 'bg-green-100 text-green-700 border border-green-300'
              : 'bg-white text-gray-600 border border-gray-300 hover:bg-green-50 hover:border-green-300'
          } ${disabled || isSubmitting ? 'opacity-50 cursor-not-allowed' : ''}`}
        >
          <span className="text-lg">🤘</span>
          <span className="text-sm font-medium">{upvotes}</span>
        </button>

        {/* Downvote Button */}
        <button
          onClick={() => handleVote('down')}
          disabled={disabled || isSubmitting}
          className={`flex items-center space-x-2 px-3 py-2 rounded-md transition-colors ${
            currentVote === 'down'
              ? 'bg-red-100 text-red-700 border border-red-300'
              : 'bg-white text-gray-600 border border-gray-300 hover:bg-red-50 hover:border-red-300'
          } ${disabled || isSubmitting ? 'opacity-50 cursor-not-allowed' : ''}`}
        >
          <span className="text-lg">👎</span>
          <span className="text-sm font-medium">{downvotes}</span>
        </button>
      </div>

      {/* Vote Summary */}
      {totalVotes > 0 && (
        <div className="text-center">
          <div className="text-sm text-gray-600">
            {votePercentage}% found this helpful
          </div>
          <div className="text-xs text-gray-500">
            {totalVotes} total votes
          </div>
        </div>
      )}

      {/* Loading State */}
      {isSubmitting && (
        <div className="text-xs text-gray-500">Submitting vote...</div>
      )}
    </div>
  );
}
