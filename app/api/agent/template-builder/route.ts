import { NextRequest, NextResponse } from "next/server";

export const runtime = "nodejs";
export const maxDuration = 60;

type TemplateSpec = { sections: string[]; build: (tab: string) => string };

const TEMPLATES: Record<string, TemplateSpec> = {
  "legal-contract": {
    sections: ["Parties", "Recitals", "Definitions", "Obligations", "Term and Termination", "Confidentiality", "Liability", "Governing Law", "Signatures"],
    build: (tab) => `# Legal Contract Template${tab ? `\n> Domain context: ${tab}` : ""}

## Parties
{{party_one}} and {{party_two}}

## Recitals
{{background_and_purpose}}

## Definitions
{{defined_terms}}

## Obligations
{{obligations_of_each_party}}

## Term and Termination
{{term_and_termination_conditions}}

## Confidentiality
{{confidentiality_terms}}

## Liability
{{limitation_of_liability}}

## Governing Law
{{jurisdiction_and_governing_law}}

## Signatures
{{signature_blocks}}`,
  },
  "business-plan": {
    sections: ["Executive Summary", "Company Overview", "Market Analysis", "Product or Service", "Business Model", "Marketing and Sales", "Operations", "Financial Plan", "Milestones"],
    build: (tab) => `# Business Plan Template${tab ? `\n> Domain context: ${tab}` : ""}

## Executive Summary
{{one_page_summary}}

## Company Overview
{{mission_vision_and_structure}}

## Market Analysis
{{market_size_segments_and_competitors}}

## Product or Service
{{offering_and_value_proposition}}

## Business Model
{{revenue_streams_and_unit_economics}}

## Marketing and Sales
{{go_to_market_strategy}}

## Operations
{{team_processes_and_tools}}

## Financial Plan
{{projections_funding_and_key_metrics}}

## Milestones
{{phased_roadmap}}`,
  },
  "research-paper": {
    sections: ["Abstract", "Introduction", "Literature Review", "Methodology", "Results", "Discussion", "Conclusion", "References"],
    build: (tab) => `# Research Paper Template${tab ? `\n> Domain context: ${tab}` : ""}

## Abstract
{{summary_of_purpose_methods_and_findings}}

## Introduction
{{background_research_question_and_objectives}}

## Literature Review
{{prior_work_and_gaps}}

## Methodology
{{data_sources_methods_and_limitations}}

## Results
{{findings_with_evidence}}

## Discussion
{{interpretation_and_implications}}

## Conclusion
{{key_takeaways_and_future_work}}

## References
{{citations}}`,
  },
};

const GENERIC: TemplateSpec = {
  sections: ["Overview", "Details", "Considerations", "Next Steps"],
  build: (tab) => `# Template${tab ? `\n> Domain context: ${tab}` : ""}

## Overview
{{purpose_and_scope}}

## Details
{{key_information}}

## Considerations
{{risks_dependencies_and_constraints}}

## Next Steps
{{actions_and_owners}}`,
};

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const type = typeof body?.type === "string" ? body.type.trim() : "";
    const tab = typeof body?.tab === "string" ? body.tab.trim() : "";
    if (!type) return NextResponse.json({ error: "type required" }, { status: 400 });

    const spec = TEMPLATES[type.toLowerCase().replace(/[\s_]+/g, "-")] || GENERIC;
    return NextResponse.json({
      template: spec.build(tab),
      type,
      sections: spec.sections,
    });
  } catch (err) {
    const message = err instanceof Error ? err.message : "Template creation failed.";
    console.error("Obi AI template request failed", { message });
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
