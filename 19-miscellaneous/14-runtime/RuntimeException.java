
/**
 * Example RuntimeException usage in a token processing context.
 * This appears to be a fragment that was extracted from a larger class.
 */
public class TokenProcessor {
    private java.util.List<String> tokens;
    
    public TokenProcessor(java.util.List<String> tokens) {
        this.tokens = tokens != null ? tokens : new java.util.ArrayList<>();
    }
    
    public String processTokens() {
        if (this.tokens.isEmpty()) {
            throw new RuntimeException("No tokens available");
        }

        if (this.tokens.size() > 1) {
            // Process multiple tokens
            return String.join(" ", this.tokens);
        } else {
            // Process single token
            return this.tokens.get(0);
        }
    }
}