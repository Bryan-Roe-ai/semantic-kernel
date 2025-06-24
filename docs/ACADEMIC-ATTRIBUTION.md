# DOI Registration and Academic Attribution Guide

## Setting Up DOI with Zenodo

### 1. Zenodo Registration
1. Visit [Zenodo.org](https://zenodo.org/)
2. Sign in with GitHub account
3. Go to GitHub integration settings
4. Enable integration for this repository

### 2. Creating a Release for DOI
```bash
# Create a tagged release
git tag -a v1.0.0 -m "Initial release for DOI registration"
git push origin v1.0.0

# Create GitHub release
# This will automatically trigger Zenodo DOI creation
```

### 3. Update Citation Files
Once DOI is assigned:
1. Update CITATION.cff with DOI identifier
2. Update README badges with DOI badge
3. Update documentation with proper citation format

## ORCID Integration

### Setting Up ORCID
1. Register at [ORCID.org](https://orcid.org/)
2. Add this software to your ORCID profile
3. Update CITATION.cff with your ORCID ID
4. Link GitHub account to ORCID

### ORCID Benefits
- Persistent researcher identification
- Academic contribution tracking
- Enhanced discoverability
- Professional credibility

## CRediT (Contributor Roles Taxonomy)

### Contributor Roles
When documenting contributions, use CRediT taxonomy:

- **Conceptualization**: Ideas, formulation of research goals
- **Data curation**: Management activities for research data
- **Formal analysis**: Statistical, mathematical analysis
- **Funding acquisition**: Acquisition of financial support
- **Investigation**: Research and investigation process
- **Methodology**: Development of methodology
- **Project administration**: Management and coordination
- **Resources**: Provision of resources
- **Software**: Programming, software development
- **Supervision**: Oversight and leadership
- **Validation**: Verification of results/experiments
- **Visualization**: Data presentation and visualization
- **Writing – original draft**: Creation of initial draft
- **Writing – review & editing**: Critical review and revision

### Implementation in Project
```yaml
# Example contributor entry with CRediT roles
contributors:
  - name: "Bryan Roe"
    orcid: "https://orcid.org/0000-0000-0000-0000"
    roles:
      - "Conceptualization"
      - "Software"
      - "Methodology"
      - "Writing – original draft"
      - "Project administration"
```

## Academic Recognition

### Citation Tracking
- Set up Google Scholar profile
- Monitor citations through Semantic Scholar
- Track repository stars and forks
- Monitor academic usage through surveys

### Publication Strategy
1. **Software Paper**: Submit to Journal of Open Source Software (JOSS)
2. **Research Paper**: Submit findings to AI/AGI conferences
3. **Workshop Presentations**: Present at relevant academic workshops
4. **Blog Posts**: Technical blog posts for broader reach

### Impact Metrics
- GitHub stars and forks
- Citation count
- Download statistics
- Academic collaboration requests
- Conference presentations

## Licensing and Attribution

### MIT License Compliance
- Maintain MIT license for compatibility
- Ensure all contributions are properly licensed
- Document third-party license requirements
- Provide clear attribution guidelines

### Attribution Requirements
When using this software:
1. Cite using CITATION.cff format
2. Include DOI when available
3. Acknowledge specific features used
4. Follow academic citation standards

---

**Next Steps:**
1. Complete ORCID registration and profile setup
2. Create GitHub release for Zenodo DOI
3. Submit to relevant software registries
4. Begin academic outreach and collaboration
