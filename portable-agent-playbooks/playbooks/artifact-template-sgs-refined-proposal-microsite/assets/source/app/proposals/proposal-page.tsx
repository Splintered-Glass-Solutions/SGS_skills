import Image from "next/image";
import Link from "next/link";
import type { ReactNode } from "react";

import { PrintButton } from "./print-button";
import { RtiRenewalDecision } from "./rti-renewal-decision";
import type {
  HourlyEngagementProposal,
  HybridAdvisorProposal,
  ProposalBilling,
  ProposalBranding,
  ProposalDiscipline,
  ProposalDocument,
  ProposalLink,
  ProposalPhase,
  ProposalReason,
  ProposalRow,
  ProposalTier,
  StrategicRetainerProposal,
  UnifiedRetainerProposal,
  WebsiteBuildProposal,
} from "./proposal-data";

type ProposalPageProps = {
  proposal: ProposalDocument;
  checkoutStatus?: "success" | "cancel" | null;
  agreementCta?: {
    label: string;
    href: string;
    caption: string;
  } | null;
  signingError?: string | null;
};

const defaultBranding: ProposalBranding = {
  wordmarkSrc: "/logos/bannerwhiteHQ.png",
  wordmarkAlt: "Splintered Glass Solutions",
  wordmarkWidth: 1980,
  wordmarkHeight: 352,
  wordmarkPanel: false,
  eyebrowPrimary: "Splintered Glass Solutions",
  eyebrowSecondary: "Proposal & Engagement Letter",
  showEmblem: true,
  introBandText:
    "This page is a proposal-only microsite intended for review and planning. Formal contract documents will follow separately if the proposal is approved.",
};

function formatSectionNumber(value: number) {
  return value.toString().padStart(2, "0");
}

function ProseSection({
  id,
  title,
  paragraphs,
  closingMarkSrc,
  closingMarkAlt,
}: {
  id: string;
  title: string;
  paragraphs: string[];
  closingMarkSrc?: string;
  closingMarkAlt?: string;
}) {
  return (
    <section className="proposal-section">
      <div className="section-heading">
        <p className="section-index">{id}</p>
        <h2>{title}</h2>
      </div>
      <div className={closingMarkSrc ? "prose-flow-with-mark" : undefined}>
        <div className="prose-flow">
          {paragraphs.map((paragraph) => (
            <p key={paragraph}>{paragraph}</p>
          ))}
        </div>
        {closingMarkSrc ? (
          <div className="closing-mark-wrap">
            <Image
              src={closingMarkSrc}
              alt={closingMarkAlt ?? ""}
              className="closing-mark"
              width={264}
              height={127}
            />
          </div>
        ) : null}
      </div>
    </section>
  );
}

function PersonalNoteSection({
  id,
  paragraphs,
}: {
  id: string;
  paragraphs: string[];
}) {
  return (
    <section className="personal-note">
      <div className="section-heading personal-note-heading">
        <p className="section-index">{id}</p>
        <h2>Personal Note</h2>
      </div>
      <div className="prose-flow personal-note-copy">
        {paragraphs.map((paragraph) => (
          <p key={paragraph}>{paragraph}</p>
        ))}
      </div>
    </section>
  );
}

function BulletSection({
  id,
  title,
  items,
}: {
  id: string;
  title: string;
  items: string[];
}) {
  return (
    <section className="proposal-section">
      <div className="section-heading">
        <p className="section-index">{id}</p>
        <h2>{title}</h2>
      </div>
      <ul className="benefit-list">
        {items.map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ul>
    </section>
  );
}

function ReasonsSection({
  id,
  title,
  reasons,
  anchorId,
}: {
  id: string;
  title: string;
  reasons: ProposalReason[];
  anchorId?: string;
}) {
  return (
    <section className="proposal-section" id={anchorId}>
      <div className="section-heading">
        <p className="section-index">{id}</p>
        <h2>{title}</h2>
      </div>
      <div className="stacked-reasons">
        {reasons.map((reason) => (
          <article key={reason.title} className="reason-block">
            <h3>{reason.title}</h3>
            <div className="prose-flow">
              {reason.paragraphs.map((paragraph) => (
                <p key={paragraph}>{paragraph}</p>
              ))}
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}

function SummaryGrid({ rows }: { rows: ProposalRow[] }) {
  const columnCount = Math.min(Math.max(rows.length, 1), 4);

  return (
    <div className={`retainer-summary summary-cols-${columnCount}`}>
      {rows.map((item) => (
        <div key={item.label}>
          <p>{item.label}</p>
          <strong>{item.value}</strong>
        </div>
      ))}
    </div>
  );
}

function DisciplineIcon({ name }: { name: NonNullable<ProposalDiscipline["icon"]> }) {
  const paths: Record<NonNullable<ProposalDiscipline["icon"]>, ReactNode> = {
    portfolio: <><path d="M4 18h16" /><path d="M6 16V9" /><path d="M12 16V5" /><path d="M18 16v-3" /></>,
    pipeline: <><path d="M4 7h5l2 3h9" /><path d="M4 7v10h16V10" /><path d="M15 14h3" /></>,
    match: <><circle cx="9" cy="9" r="4" /><path d="m12 12 6 6" /><path d="M16 5v4M14 7h4" /></>,
    filter: <><path d="M4 5h16l-6 7v5l-4 2v-7z" /></>,
    data: <><ellipse cx="12" cy="6" rx="7" ry="3" /><path d="M5 6v6c0 1.7 3.1 3 7 3s7-1.3 7-3V6" /><path d="M5 12v6c0 1.7 3.1 3 7 3s7-1.3 7-3v-6" /></>,
    workflow: <><rect x="4" y="4" width="5" height="5" rx="1" /><rect x="15" y="15" width="5" height="5" rx="1" /><path d="M9 6h4a3 3 0 0 1 3 3v6" /></>,
    people: <><circle cx="9" cy="8" r="3" /><path d="M3.5 19a5.5 5.5 0 0 1 11 0" /><path d="M16 5.5a3 3 0 0 1 0 5.8M17 14a5 5 0 0 1 4 5" /></>,
    shield: <><path d="M12 3 19 6v5c0 4.4-2.9 8.2-7 10-4.1-1.8-7-5.6-7-10V6z" /><path d="m9 12 2 2 4-4" /></>,
  };

  return (
    <span className="discipline-icon" aria-hidden="true">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round">
        {paths[name]}
      </svg>
    </span>
  );
}

function DisciplineGrid({
  items,
  className,
}: {
  items: ProposalDiscipline[];
  className?: string;
}) {
  return (
    <div className={className ? `discipline-grid ${className}` : "discipline-grid"}>
      {items.map((item) => (
        <article key={item.title} className="discipline-block">
          {item.icon ? <DisciplineIcon name={item.icon} /> : null}
          <h3>{item.title}</h3>
          <p>{item.description}</p>
        </article>
      ))}
    </div>
  );
}

function TierGrid({
  tiers,
  variant,
}: {
  tiers: ProposalTier[];
  variant?: "package";
}) {
  const gridClassName = [
    "tier-grid",
    `tier-grid-${tiers.length}`,
    variant === "package" ? "tier-grid-package" : null,
  ]
    .filter(Boolean)
    .join(" ");

  return (
    <div className={gridClassName}>
      {tiers.map((tier) => (
        <article
          key={tier.name}
          className={tier.recommended ? "tier-card tier-card-recommended" : "tier-card"}
        >
          <div className="tier-head">
            <div>
              {tier.recommended ? <p className="tier-badge">Recommended</p> : null}
              {tier.priceLabel ? <p className="tier-price-label">{tier.priceLabel}</p> : null}
              <p className="tier-name">{tier.name}</p>
              <h3>{tier.monthlyFee}</h3>
              {tier.priceCaption ? (
                <p className="tier-price-caption">{tier.priceCaption}</p>
              ) : null}
            </div>
            {tier.discount ? (
              <p className="tier-discount">{tier.discount}</p>
            ) : null}
          </div>

          <dl className="tier-meta">
            <div>
              <dt>{tier.hoursLabel ?? "Monthly Capacity"}</dt>
              <dd>{tier.hours}</dd>
            </div>
            {tier.effectiveRate ? (
              <div>
                <dt>Effective Rate</dt>
                <dd>{tier.effectiveRate}</dd>
              </div>
            ) : null}
          </dl>

          <p className="tier-best-for">{tier.bestFor}</p>

          <ul className="benefit-list tier-list">
            {tier.allocation.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </article>
      ))}
    </div>
  );
}

function PhaseGrid({
  phases,
}: {
  phases: ProposalPhase[];
}) {
  return (
    <div className="phase-grid">
      {phases.map((phase) => (
        <article key={phase.phase} className="phase-card">
          <p className="phase-label">{phase.phase}</p>
          <h3>{phase.title}</h3>
          <p>{phase.description}</p>
        </article>
      ))}
    </div>
  );
}

function DualListSection({
  id,
  leftTitle,
  leftItems,
  rightTitle,
  rightItems,
}: {
  id: string;
  leftTitle: string;
  leftItems: string[];
  rightTitle: string;
  rightItems: string[];
}) {
  return (
    <section className="proposal-section">
      <div className="section-heading">
        <p className="section-index">{id}</p>
        <h2>Scope Boundaries</h2>
      </div>
      <div className="dual-list-grid">
        <article className="discipline-block dual-list-card">
          <h3>{leftTitle}</h3>
          <ul className="benefit-list">
            {leftItems.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </article>
        <article className="discipline-block dual-list-card">
          <h3>{rightTitle}</h3>
          <ul className="benefit-list">
            {rightItems.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </article>
      </div>
    </section>
  );
}

function RecommendationSection({
  id,
  title,
  recommendation,
  anchorId,
}: {
  id: string;
  title: string;
  recommendation: StrategicRetainerProposal["recommendation"];
  anchorId?: string;
}) {
  return (
    <section className="proposal-section recommendation-section" id={anchorId}>
      <div className="section-heading">
        <p className="section-index">{id}</p>
        <h2>{title}</h2>
      </div>
      <div className="recommendation-grid">
        <article className="recommendation-card">
          <p className="tier-name">Recommendation</p>
          <h3>{recommendation.title}</h3>
          <p>{recommendation.body}</p>
        </article>
        <article className="discipline-block">
          <h3>Next Steps</h3>
          <ul className="benefit-list">
            {recommendation.nextSteps.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </article>
      </div>
    </section>
  );
}

function ResourceLinksSection({
  id,
  title,
  links,
}: {
  id: string;
  title: string;
  links: ProposalLink[];
}) {
  return (
    <section className="proposal-section">
      <div className="section-heading">
        <p className="section-index">{id}</p>
        <h2>{title}</h2>
      </div>
      <div className="stacked-reasons">
        {links.map((link) => (
          <article key={link.url} className="reason-block resource-link-card">
            <h3>
              <a href={link.url} target="_blank" rel="noreferrer">
                {link.label}
              </a>
            </h3>
            {link.description ? (
              <div className="prose-flow">
                <p>{link.description}</p>
              </div>
            ) : null}
            <p className="resource-link-action">
              <a href={link.url} target="_blank" rel="noreferrer">
                Open material <span aria-hidden="true">↗</span>
              </a>
            </p>
          </article>
        ))}
      </div>
    </section>
  );
}

function JeffersonDecisionBrief() {
  const facts = [
    { label: "What it is", value: "City-sponsored business strategy" },
    { label: "Recommended seat", value: "$20,000 combined review" },
    { label: "Business cost", value: "$0" },
    { label: "First step", value: "Start with Duke's business" },
  ];

  return (
    <section className="jefferson-decision-brief" aria-labelledby="jefferson-decision-title">
      <div className="jefferson-decision-copy">
        <p className="jefferson-decision-label">Decision brief</p>
        <h2 id="jefferson-decision-title">
          A practical way for Jefferson to invest in stronger local businesses.
        </h2>
        <p>
          Sponsor enterprise-grade strategy for a small pilot, begin with one local proof point,
          and expand only if the results justify it.
        </p>
      </div>

      <dl className="jefferson-decision-facts">
        {facts.map((fact) => (
          <div key={fact.label}>
            <dt>{fact.label}</dt>
            <dd>{fact.value}</dd>
          </div>
        ))}
      </dl>

      <nav className="jefferson-jump-links" aria-label="Jump to proposal sections">
        <a href="#why-jefferson">Why it matters</a>
        <a href="#review-options">Review options</a>
        <a href="#city-pilot">Pilot structure</a>
        <a href="#recommended-next-step">First step</a>
      </nav>
    </section>
  );
}

function ApprovalSection({
  proposal,
  billing,
  checkoutStatus,
  agreementCta,
}: {
  proposal: ProposalDocument;
  billing?: ProposalBilling | null;
  checkoutStatus?: "success" | "cancel" | null;
  agreementCta?: ProposalPageProps["agreementCta"];
}) {
  const hasAgreement = Boolean(agreementCta);
  const hasBilling = Boolean(billing);

  return (
    <section className="proposal-section billing-panel">
      <div className="section-heading">
        <p className="section-index">00</p>
        <h2>Approval &amp; Next Steps</h2>
      </div>
      <div className="billing-copy">
        {hasAgreement && hasBilling && billing ? (
          <p>
            If this direction looks right, there are two steps to get started: sign the retainer
            agreement, then start the {billing.termMonths}-month Stripe checkout at $
            {(billing.unitAmount / 100).toLocaleString()}/month.
          </p>
        ) : hasBilling && billing ? (
          <p>
            If this direction looks right, use the hosted checkout below to start the{" "}
            {billing.termMonths}-month retainer at ${(billing.unitAmount / 100).toLocaleString()}/
            month. The formal contract will follow separately by email.
          </p>
        ) : (
          <p>Review and sign the agreement when you are ready to move forward.</p>
        )}
      </div>

      <div className={hasAgreement && hasBilling ? "approval-actions-grid" : "billing-cta-row"}>
        {agreementCta ? (
          <div className="approval-step-card">
            <p className="approval-step-label">Step 1</p>
            <a className="billing-cta" href={agreementCta.href}>
              {agreementCta.label}
            </a>
            <p className="billing-caption">{agreementCta.caption}</p>
          </div>
        ) : null}

        {billing ? (
          <div className="approval-step-card">
            <p className="approval-step-label">{agreementCta ? "Step 2" : "Payment"}</p>
            <Link className="billing-cta" href={`/proposals/${proposal.slug}/checkout`}>
              {billing.ctaLabel}
            </Link>
            <p className="billing-caption">
              Hosted by Stripe. {billing.termMonths} monthly charges, then auto-stop.
            </p>
          </div>
        ) : null}
      </div>
      {billing && checkoutStatus === "success" ? (
        <p className="checkout-status checkout-status-success">
          Checkout completed. Once Stripe confirms payment, the retainer will be scheduled to end
          automatically after {billing.termMonths} monthly charges.
        </p>
      ) : null}
      {billing && checkoutStatus === "cancel" ? (
        <p className="checkout-status checkout-status-cancel">
          Checkout was canceled. You can return to this page and restart the billing flow at any
          time.
        </p>
      ) : null}
    </section>
  );
}

function AgreementCtaSection({
  cta,
  variant = "primary",
}: {
  cta: NonNullable<ProposalPageProps["agreementCta"]>;
  variant?: "primary" | "closing";
}) {
  const isSignedReview = cta.label.toLowerCase().includes("signed");
  const heading =
    variant === "closing"
      ? isSignedReview
        ? "Signed Agreement"
        : "Ready To Sign"
      : isSignedReview
        ? "Agreement Complete"
        : "Agreement Signature";
  const copy =
    variant === "closing"
      ? isSignedReview
        ? "Review the completed agreement and download a copy for your records."
        : "Review and sign the agreement when you are ready to move forward."
      : cta.caption;

  return (
    <section
      className={`proposal-section signing-proposal-panel ${
        variant === "closing" ? "signing-proposal-panel-closing" : ""
      }`}
    >
      <div className="signing-proposal-content">
        <div>
          <div className="section-heading">
            <p className="section-index">{variant === "closing" ? "Next" : "00"}</p>
            <h2>{heading}</h2>
          </div>
          <div className="billing-copy">
            <p>{copy}</p>
          </div>
        </div>
        <div className="billing-cta-row signing-proposal-action">
          <a className="billing-cta" href={cta.href}>
            {cta.label}
          </a>
        </div>
      </div>
    </section>
  );
}

function UnifiedProposalBody({
  proposal,
  startIndex,
}: {
  proposal: UnifiedRetainerProposal;
  startIndex: number;
}) {
  return (
    <>
      <ReasonsSection
        id={formatSectionNumber(startIndex)}
        title={proposal.rationaleHeading}
        reasons={proposal.rationale}
      />

      <section className="proposal-section">
        <div className="section-heading">
          <p className="section-index">{formatSectionNumber(startIndex + 1)}</p>
          <h2>Proposed Retainer Structure</h2>
        </div>
        <SummaryGrid rows={proposal.retainerSummary} />
        <DisciplineGrid items={proposal.disciplines} />
        <p className="section-note">{proposal.retainerFlexNote}</p>
      </section>

      <section className="proposal-section">
        <div className="section-heading">
          <p className="section-index">{formatSectionNumber(startIndex + 2)}</p>
          <h2>Current Engagement vs. Proposed Engagement</h2>
        </div>

        <div className="comparison-block print-keep">
          <div className="table-wrap desktop-only">
            <table className="comparison-table">
              <thead>
                <tr>
                  <th>Current Engagement</th>
                  <th>Monthly Cost</th>
                </tr>
              </thead>
              <tbody>
                {proposal.comparison.current.map((row) => (
                  <tr key={row.label}>
                    <td>{row.label}</td>
                    <td>{row.value}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="table-wrap desktop-only">
            <table className="comparison-table">
              <thead>
                <tr>
                  <th>Proposed Engagement</th>
                  <th>Monthly Cost</th>
                </tr>
              </thead>
              <tbody>
                {proposal.comparison.proposed.map((row) => (
                  <tr key={row.label}>
                    <td>{row.label}</td>
                    <td>{row.value}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="comparison-mobile mobile-only">
            {[...proposal.comparison.current, ...proposal.comparison.proposed].map(
              (row) => (
                <div key={row.label} className="comparison-mobile-row">
                  <p>{row.label}</p>
                  <strong>{row.value}</strong>
                </div>
              ),
            )}
          </div>
        </div>

        <div className="highlight-statement">
          <strong>{proposal.comparison.savingsHeadline}</strong>
          <p>{proposal.comparison.summary}</p>
        </div>
      </section>

      <section className="proposal-section print-keep">
        <div className="section-heading">
          <p className="section-index">{formatSectionNumber(startIndex + 3)}</p>
          <h2>Initial Monthly Planning Estimate</h2>
        </div>

        <div className="table-wrap desktop-only">
          <table className="planning-table">
            <thead>
              <tr>
                <th>Month</th>
                <th>Design</th>
                <th>Development</th>
                <th>Marketing</th>
                <th>Total</th>
                <th>Core Focus</th>
              </tr>
            </thead>
            <tbody>
              {proposal.monthlyPlan.map((month) => (
                <tr key={month.month}>
                  <td>{month.month}</td>
                  <td>{month.design}</td>
                  <td>{month.development}</td>
                  <td>{month.marketing}</td>
                  <td>{month.total}</td>
                  <td>{month.focus}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="planning-mobile mobile-only">
          {proposal.monthlyPlan.map((month) => (
            <article key={month.month} className="month-card">
              <div className="month-card-head">
                <h3>{month.month}</h3>
                <strong>{month.total} hours</strong>
              </div>
              <dl>
                <div>
                  <dt>Design</dt>
                  <dd>{month.design}</dd>
                </div>
                <div>
                  <dt>Development</dt>
                  <dd>{month.development}</dd>
                </div>
                <div>
                  <dt>Marketing</dt>
                  <dd>{month.marketing}</dd>
                </div>
              </dl>
              <p>{month.focus}</p>
            </article>
          ))}
        </div>

        <div className="prose-flow section-note">
          {proposal.allocationNote.map((paragraph) => (
            <p key={paragraph}>{paragraph}</p>
          ))}
        </div>
      </section>

      <ProseSection
        id={formatSectionNumber(startIndex + 4)}
        title="Timeline Narrative"
        paragraphs={proposal.timelineNarrative}
      />

      <BulletSection
        id={formatSectionNumber(startIndex + 5)}
        title="Client Benefits"
        items={proposal.clientBenefits}
      />

      <ProseSection
        id={formatSectionNumber(startIndex + 6)}
        title="Closing Note"
        paragraphs={proposal.closingNote}
      />
    </>
  );
}

function HybridProposalBody({
  proposal,
  startIndex,
}: {
  proposal: HybridAdvisorProposal;
  startIndex: number;
}) {
  return (
    <>
      <ReasonsSection
        id={formatSectionNumber(startIndex)}
        title={proposal.rationaleHeading}
        reasons={proposal.rationale}
      />

      <section className="proposal-section">
        <div className="section-heading">
          <p className="section-index">{formatSectionNumber(startIndex + 1)}</p>
          <h2>{proposal.focusHeading}</h2>
        </div>
        <DisciplineGrid items={proposal.focusAreas} />
      </section>

      <section className="proposal-section">
        <div className="section-heading">
          <p className="section-index">{formatSectionNumber(startIndex + 2)}</p>
          <h2>Engagement Structure</h2>
        </div>
        <SummaryGrid rows={proposal.engagementSummary} />
        <DisciplineGrid items={proposal.engagementTracks} />
        <p className="section-note">{proposal.engagementNote}</p>
      </section>

      <section className="proposal-section">
        <div className="section-heading">
          <p className="section-index">{formatSectionNumber(startIndex + 3)}</p>
          <h2>{proposal.equityHeading}</h2>
        </div>
        <SummaryGrid rows={proposal.equitySummary} />
        <div className="prose-flow">
          {proposal.equityDetails.map((paragraph) => (
            <p key={paragraph}>{paragraph}</p>
          ))}
        </div>
      </section>

      <section className="proposal-section">
        <div className="section-heading">
          <p className="section-index">{formatSectionNumber(startIndex + 4)}</p>
          <h2>{proposal.roadmapHeading}</h2>
        </div>
        <PhaseGrid phases={proposal.roadmap} />
        {proposal.roadmapNote ? <p className="section-note">{proposal.roadmapNote}</p> : null}
      </section>

      <section className="proposal-section">
        <div className="section-heading">
          <p className="section-index">{formatSectionNumber(startIndex + 5)}</p>
          <h2>Execution Retainer Options</h2>
        </div>
        <TierGrid tiers={proposal.tiers} />
      </section>

      <ReasonsSection
        id={formatSectionNumber(startIndex + 6)}
        title={proposal.partnerHeading}
        reasons={proposal.partnerReasons}
      />

      <BulletSection
        id={formatSectionNumber(startIndex + 7)}
        title="Engagement Mechanics"
        items={proposal.mechanics}
      />

      <BulletSection
        id={formatSectionNumber(startIndex + 8)}
        title="Client Benefits"
        items={proposal.clientBenefits}
      />

      <ProseSection
        id={formatSectionNumber(startIndex + 9)}
        title="Closing Note"
        paragraphs={proposal.closingNote}
      />
    </>
  );
}

function HourlyEngagementBody({
  proposal,
  startIndex,
}: {
  proposal: HourlyEngagementProposal;
  startIndex: number;
}) {
  let sectionIndex = startIndex;
  const nextId = () => formatSectionNumber(sectionIndex++);

  return (
    <>
      <ReasonsSection
        id={nextId()}
        title={proposal.rationaleHeading}
        reasons={proposal.rationale}
      />

      {proposal.engagementSummaryHeading && proposal.engagementSummary?.length ? (
        <section className="proposal-section">
          <div className="section-heading">
            <p className="section-index">{nextId()}</p>
            <h2>{proposal.engagementSummaryHeading}</h2>
          </div>
          <SummaryGrid rows={proposal.engagementSummary} />
        </section>
      ) : null}

      <section className="proposal-section">
        <div className="section-heading">
          <p className="section-index">{nextId()}</p>
          <h2>{proposal.focusHeading}</h2>
        </div>
        <DisciplineGrid items={proposal.focusAreas} />
      </section>

      {proposal.workingQuestionsHeading && proposal.workingQuestions ? (
        <section className="proposal-section">
          <div className="section-heading">
            <p className="section-index">{nextId()}</p>
            <h2>{proposal.workingQuestionsHeading}</h2>
          </div>
          <DisciplineGrid items={proposal.workingQuestions} />
        </section>
      ) : null}

      {proposal.agendaHeading && proposal.agenda ? (
        <section className="proposal-section">
          <div className="section-heading">
            <p className="section-index">{nextId()}</p>
            <h2>{proposal.agendaHeading}</h2>
          </div>
          <PhaseGrid phases={proposal.agenda} />
        </section>
      ) : null}

      <BulletSection
        id={nextId()}
        title={proposal.mechanicsHeading}
        items={proposal.mechanics}
      />

      <BulletSection
        id={nextId()}
        title={proposal.assumptionsHeading}
        items={proposal.assumptions}
      />

      <BulletSection
        id={nextId()}
        title={proposal.nextStepsHeading}
        items={proposal.nextSteps}
      />

      <BulletSection
        id={nextId()}
        title="Client Benefits"
        items={proposal.clientBenefits}
      />

      {proposal.packageOptionsHeading && proposal.packageOptions ? (
        <section className="proposal-section">
          <div className="section-heading">
            <p className="section-index">{nextId()}</p>
            <h2>{proposal.packageOptionsHeading}</h2>
          </div>
          <TierGrid tiers={proposal.packageOptions} variant="package" />
        </section>
      ) : null}

      <ProseSection
        id={nextId()}
        title="Closing Note"
        paragraphs={proposal.closingNote}
      />
    </>
  );
}

function StrategicRetainerBody({
  proposal,
  startIndex,
  signingError,
}: {
  proposal: StrategicRetainerProposal;
  startIndex: number;
  signingError?: string | null;
}) {
  const compact = proposal.slug === "dry-ground-investments";
  const hasSetup = Boolean(
    proposal.setupHeading && proposal.setupSummary && proposal.setupDetails,
  );
  const hasResourceLinks = Boolean(proposal.resourceLinksHeading && proposal.resourceLinks);
  const hasRationale = proposal.rationale.length > 0;
  const hasImmediateValue = Boolean(
    proposal.immediateValueHeading && proposal.immediateValueIntro && proposal.immediateValue?.length,
  );
  const hasFocusAreas = proposal.focusAreas.length > 0;
  const hasIncludedSupport = proposal.includedSupport.length > 0;
  const hasPartnershipReasons = proposal.partnershipReasons.length > 0;
  const hasClientBenefits = proposal.clientBenefits.length > 0;
  const hasClosingNote = proposal.closingNote.length > 0;
  let sectionIndex = startIndex;
  const nextId = () => formatSectionNumber(sectionIndex++);

  return (
    <>
      {hasImmediateValue ? (
        <section className="proposal-section immediate-value-section" id={compact ? "value" : undefined}>
          <div className="section-heading">
            <p className="section-index">{nextId()}</p>
            <h2>{proposal.immediateValueHeading}</h2>
          </div>
          <p className="immediate-value-intro">{proposal.immediateValueIntro}</p>
          <DisciplineGrid items={proposal.immediateValue!} className="immediate-value-grid" />
        </section>
      ) : null}

      {hasRationale ? (
        <ReasonsSection
          id={nextId()}
          title={proposal.rationaleHeading}
          reasons={proposal.rationale}
          anchorId={compact ? "why-now" : proposal.slug === "jefferson-on-track" ? "why-jefferson" : undefined}
        />
      ) : null}

      <section
        className="proposal-section"
        id={compact ? "options" : proposal.slug === "jefferson-on-track" ? "review-options" : undefined}
      >
        <div className="section-heading">
          <p className="section-index">{nextId()}</p>
          <h2>{proposal.optionsHeading}</h2>
        </div>
        <TierGrid tiers={proposal.tiers} />
      </section>

      {proposal.slug === "rti-renewal" ? (
        <RtiRenewalDecision error={signingError} />
      ) : null}

      {hasSetup ? (
        <section
          className="proposal-section"
          id={proposal.slug === "jefferson-on-track" ? "city-pilot" : undefined}
        >
          <div className="section-heading">
            <p className="section-index">{nextId()}</p>
            <h2>{proposal.setupHeading}</h2>
          </div>
          <SummaryGrid rows={proposal.setupSummary!} />
          <div className="prose-flow">
            {proposal.setupDetails!.map((paragraph) => (
              <p key={paragraph}>{paragraph}</p>
            ))}
          </div>
        </section>
      ) : null}

      {proposal.timelineHeading && proposal.timeline ? (
        <section className="proposal-section" id={compact ? "roadmap" : undefined}>
          <div className="section-heading">
            <p className="section-index">{nextId()}</p>
            <h2>{proposal.timelineHeading}</h2>
          </div>
          <PhaseGrid phases={proposal.timeline} />
        </section>
      ) : null}

      {hasFocusAreas ? (
        <section className="proposal-section" id={compact ? "workstreams" : undefined}>
          <div className="section-heading">
            <p className="section-index">{nextId()}</p>
            <h2>{proposal.focusHeading}</h2>
          </div>
          <DisciplineGrid
            items={proposal.focusAreas}
            className="force-leading-divider"
          />
        </section>
      ) : null}

      {hasIncludedSupport && !compact ? (
        <BulletSection
          id={nextId()}
          title={proposal.includedSupportHeading}
          items={proposal.includedSupport}
        />
      ) : null}

      {hasResourceLinks ? (
        <ResourceLinksSection
          id={nextId()}
          title={proposal.resourceLinksHeading!}
          links={proposal.resourceLinks!}
        />
      ) : null}

      {hasPartnershipReasons && !compact ? (
        <BulletSection
          id={nextId()}
          title={proposal.partnershipHeading}
          items={proposal.partnershipReasons}
        />
      ) : null}

      <RecommendationSection
        id={nextId()}
        title="Recommended Next Step"
        recommendation={proposal.recommendation}
        anchorId={compact ? "next-step" : proposal.slug === "jefferson-on-track" ? "recommended-next-step" : undefined}
      />

      {compact && hasPartnershipReasons ? (
        <details className="proposal-guardrails">
          <summary>Working boundaries</summary>
          <ul className="benefit-list">
            {proposal.partnershipReasons.map((item) => <li key={item}>{item}</li>)}
          </ul>
        </details>
      ) : null}

      {hasClientBenefits && !compact ? (
        <BulletSection
          id={nextId()}
          title="Client Benefits"
          items={proposal.clientBenefits}
        />
      ) : null}

      {hasClosingNote ? (
        <ProseSection
          id={nextId()}
          title="Closing Note"
          paragraphs={proposal.closingNote}
          closingMarkSrc={proposal.closingMarkSrc}
          closingMarkAlt={proposal.closingMarkAlt}
        />
      ) : null}
    </>
  );
}

function WebsiteBuildBody({
  proposal,
  startIndex,
}: {
  proposal: WebsiteBuildProposal;
  startIndex: number;
}) {
  return (
    <>
      <BulletSection
        id={formatSectionNumber(startIndex)}
        title={proposal.goalsHeading}
        items={proposal.goals}
      />

      <DualListSection
        id={formatSectionNumber(startIndex + 1)}
        leftTitle={proposal.scopeHeading}
        leftItems={proposal.scope}
        rightTitle={proposal.deliverablesHeading}
        rightItems={proposal.deliverables}
      />

      <section className="proposal-section">
        <div className="section-heading">
          <p className="section-index">{formatSectionNumber(startIndex + 2)}</p>
          <h2>{proposal.timelineHeading}</h2>
        </div>
        <PhaseGrid phases={proposal.timeline} />
      </section>

      <DualListSection
        id={formatSectionNumber(startIndex + 3)}
        leftTitle={proposal.includedHeading}
        leftItems={proposal.included}
        rightTitle={proposal.excludedHeading}
        rightItems={proposal.excluded}
      />

      <BulletSection
        id={formatSectionNumber(startIndex + 4)}
        title={proposal.assumptionsHeading}
        items={proposal.assumptions}
      />

      <BulletSection
        id={formatSectionNumber(startIndex + 5)}
        title="Client Benefits"
        items={proposal.clientBenefits}
      />

      <ProseSection
        id={formatSectionNumber(startIndex + 6)}
        title="Closing Note"
        paragraphs={proposal.closingNote}
      />
    </>
  );
}

export function ProposalPage({
  proposal,
  checkoutStatus,
  agreementCta,
  signingError,
}: ProposalPageProps) {
  const overviewIndex = proposal.personalNote ? 2 : 1;
  const bodyStartIndex = overviewIndex + 1;
  const branding = proposal.branding ?? defaultBranding;
  const billing =
    proposal.billing?.enabled && proposal.billing.provider === "stripe" ? proposal.billing : null;
  const shellClassName = [
    "proposal-shell",
    proposal.theme === "refined" ? "proposal-refined" : null,
    `proposal-${proposal.slug}`,
  ]
    .filter(Boolean)
    .join(" ");

  return (
    <main className={shellClassName}>
      <section className="cover">
        <div className="cover-brand">
          <div className={branding.wordmarkPanel ? "cover-wordmark-panel" : undefined}>
            {branding.wordmarkMode === "icon-text" && branding.wordmarkText && branding.wordmarkIconSrc ? (
              <div className="cover-wordmark-lockup" aria-label={branding.wordmarkAlt}>
                <Image
                  src={branding.wordmarkIconSrc}
                  alt=""
                  aria-hidden="true"
                  className="cover-wordmark-icon"
                  width={264}
                  height={127}
                  priority
                />
                <span className="cover-wordmark-text">{branding.wordmarkText}</span>
              </div>
            ) : (
              <Image
                src={branding.wordmarkSrc}
                alt={branding.wordmarkAlt}
                className="cover-wordmark"
                width={branding.wordmarkWidth}
                height={branding.wordmarkHeight}
                priority
              />
            )}
          </div>
          <div>
            <p className="eyebrow">{branding.eyebrowPrimary}</p>
            <p className="eyebrow">{branding.eyebrowSecondary}</p>
          </div>
        </div>

        <div className="cover-actions" aria-label="Proposal actions">
          <PrintButton />
        </div>

        <div className="cover-grid">
          <div className="cover-copy">
            <p className="cover-kicker">Prepared for {proposal.clientName}</p>
            <h1>{proposal.title}</h1>
            <p className="cover-date">Prepared on {proposal.preparedOn}</p>
            <p className="cover-summary">{proposal.summary}</p>
          </div>

          <div className="cover-facts">
            <dl>
              {proposal.coverFacts.map((fact) => (
                <div key={fact.label}>
                  <dt>{fact.label}</dt>
                  <dd>{fact.value}</dd>
                </div>
              ))}
            </dl>
          </div>
        </div>

        {branding.showEmblem ? (
          <Image
            src="/logos/socialInv.png"
            alt=""
            aria-hidden="true"
            className="cover-emblem"
            width={6730}
            height={6730}
            priority
          />
        ) : null}
      </section>

      {proposal.slug === "dry-ground-investments" ? (
        <nav className="proposal-jump-nav" aria-label="Proposal sections">
          <span>On this page</span>
          <a href="#value"><b>01</b>Value</a>
          <a href="#options"><b>02</b>Options</a>
          <a href="#roadmap"><b>03</b>Roadmap</a>
          <a href="#workstreams"><b>04</b>Build around</a>
          <a href="#next-step"><b>05</b>Next step</a>
        </nav>
      ) : null}

      <div className="proposal-frame">
        {billing || agreementCta ? (
          <ApprovalSection
            proposal={proposal}
            billing={billing}
            checkoutStatus={checkoutStatus}
            agreementCta={agreementCta}
          />
        ) : null}

        {proposal.personalNote ? (
          <PersonalNoteSection
            id="01"
            paragraphs={proposal.personalNote}
          />
        ) : null}

        {proposal.slug === "jefferson-on-track" ? <JeffersonDecisionBrief /> : null}

        <ProseSection
          id={formatSectionNumber(overviewIndex)}
          title="Overview"
          paragraphs={proposal.overview}
        />

        {proposal.kind === "unified" ? (
          <UnifiedProposalBody
            proposal={proposal}
            startIndex={bodyStartIndex}
          />
        ) : null}

        {proposal.kind === "hybrid-advisor" ? (
          <HybridProposalBody
            proposal={proposal}
            startIndex={bodyStartIndex}
          />
        ) : null}

        {proposal.kind === "strategic-retainer" ? (
        <StrategicRetainerBody
          proposal={proposal}
          startIndex={bodyStartIndex}
          signingError={signingError}
        />
      ) : null}

        {proposal.kind === "website-build" ? (
          <WebsiteBuildBody
            proposal={proposal}
            startIndex={bodyStartIndex}
          />
        ) : null}

        {proposal.kind === "hourly-engagement" ? (
          <HourlyEngagementBody
            proposal={proposal}
            startIndex={bodyStartIndex}
          />
        ) : null}

        {agreementCta && !billing ? (
          <AgreementCtaSection
            cta={agreementCta}
            variant="closing"
          />
        ) : null}

      </div>
    </main>
  );
}
