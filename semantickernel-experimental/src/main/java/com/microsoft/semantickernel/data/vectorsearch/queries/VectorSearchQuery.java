// Copyright (c) Microsoft. All rights reserved.
package com.microsoft.semantickernel.data.vectorsearch.queries;

import com.microsoft.semantickernel.data.vectorstorage.options.VectorSearchOptions;

import java.util.List;

public class VectorSearchQuery {
    private final VectorSearchQueryType queryType;
    private final VectorSearchOptions searchOptions;

    public VectorSearchQuery(VectorSearchQueryType queryType, VectorSearchOptions searchOptions) {
        this.queryType = queryType;
        this.searchOptions = searchOptions;
    }

    public VectorSearchQueryType getQueryType() {
        return queryType;
    }

    public VectorSearchOptions getSearchOptions() {
        return searchOptions;
    }

    public static VectorizedSearchQuery createQuery(List<Float> vector,
        VectorSearchOptions options) {
        return new VectorizedSearchQuery(vector, options);
    }

    public static VectorizableTextSearchQuery createQuery(String searchText,
        VectorSearchOptions options) {
        return new VectorizableTextSearchQuery(searchText, options);
    }
}