'use client'

import { useIntl } from '@/components/providers/intl-provider'

export default function AboutPage() {
  const { t } = useIntl()

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-center mb-8 text-text-primary dark:text-text-primary-dark">
          {t('about.title')}
        </h1>

        <div className="prose prose-lg dark:prose-invert max-w-none">
          <section className="mb-8">
            <h2 className="text-2xl font-semibold mb-4 text-text-primary dark:text-text-primary-dark">
              {t('about.mission.title')}
            </h2>
            <p className="text-text-secondary dark:text-text-secondary-dark leading-relaxed">
              {t('about.mission.description')}
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold mb-4 text-text-primary dark:text-text-primary-dark">
              {t('about.vision.title')}
            </h2>
            <p className="text-text-secondary dark:text-text-secondary-dark leading-relaxed">
              {t('about.vision.description')}
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold mb-4 text-text-primary dark:text-text-primary-dark">
              {t('about.features.title')}
            </h2>
            <div className="grid md:grid-cols-2 gap-6">
              <div className="bg-card dark:bg-card-dark p-6 rounded-lg">
                <h3 className="text-lg font-medium mb-2 text-text-primary dark:text-text-primary-dark">
                  {t('about.features.comprehensive.title')}
                </h3>
                <p className="text-text-secondary dark:text-text-secondary-dark">
                  {t('about.features.comprehensive.description')}
                </p>
              </div>
              <div className="bg-card dark:bg-card-dark p-6 rounded-lg">
                <h3 className="text-lg font-medium mb-2 text-text-primary dark:text-text-primary-dark">
                  {t('about.features.realtime.title')}
                </h3>
                <p className="text-text-secondary dark:text-text-secondary-dark">
                  {t('about.features.realtime.description')}
                </p>
              </div>
              <div className="bg-card dark:bg-card-dark p-6 rounded-lg">
                <h3 className="text-lg font-medium mb-2 text-text-primary dark:text-text-primary-dark">
                  {t('about.features.open.title')}
                </h3>
                <p className="text-text-secondary dark:text-text-secondary-dark">
                  {t('about.features.open.description')}
                </p>
              </div>
              <div className="bg-card dark:bg-card-dark p-6 rounded-lg">
                <h3 className="text-lg font-medium mb-2 text-text-primary dark:text-text-primary-dark">
                  {t('about.features.community.title')}
                </h3>
                <p className="text-text-secondary dark:text-text-secondary-dark">
                  {t('about.features.community.description')}
                </p>
              </div>
            </div>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold mb-4 text-text-primary dark:text-text-primary-dark">
              {t('about.team.title')}
            </h2>
            <p className="text-text-secondary dark:text-text-secondary-dark leading-relaxed">
              {t('about.team.description')}
            </p>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-semibold mb-4 text-text-primary dark:text-text-primary-dark">
              {t('about.contact.title')}
            </h2>
            <div className="bg-card dark:bg-card-dark p-6 rounded-lg">
              <p className="text-text-secondary dark:text-text-secondary-dark mb-4">
                {t('about.contact.description')}
              </p>
              <div className="flex flex-wrap gap-4">
                <a
                  href="mailto:contact@agentpedia.com"
                  className="text-accent dark:text-accent-dark hover:underline"
                >
                  contact@agentpedia.com
                </a>
              </div>
            </div>
          </section>
        </div>
      </div>
    </div>
  )
}