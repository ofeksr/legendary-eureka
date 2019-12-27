import click

from legendary_eureka import Glassdoor, Linkedin, Indeed

# TODO: fix echo hebrew results - translate to english?


def echo_dict_of_jobs(jobs):
    for j_title, j_link in jobs.items():
        click.echo(f'{j_title}:\n{j_link}')


def get_linkedin(url):
    linkedin = Linkedin()
    jobs = linkedin.get_jobs(url=url)
    echo_dict_of_jobs(jobs)


def get_glassdoor(job_title, job_type, job_location):
    glassdoor = Glassdoor()
    jobs = glassdoor.get_jobs(job_title=job_title, job_type=job_type, job_location=job_location)
    echo_dict_of_jobs(jobs)


def get_indeed(job_title, job_location):
    indeed = Indeed()
    jobs = indeed.get_jobs(what=job_title, where=job_location)
    echo_dict_of_jobs(jobs)


@click.command()
@click.option('-r', '--resource', 'resource', type=str,
              help='[Linkedin, Indeed, Glassdoor]')
@click.option('-t', '--type', 'job_type', type=str,
              help='For glassdoor: [fulltime, parttime, contract, internship, temporary, apprenticeship, entrylevel]')
@click.option('-l', '--location', 'job_location', type=str,
              help='For Indeed and Glassdoor: city name in Israel')
@click.option('-t', '--title', 'job_title', type=str, help='Required for: [Indeed, Glassdoor]')
@click.option('-u', '--url', 'url', type=str,
              help='For Linkedin: url of job position to search similar jobs')
def cli_get_jobs(resource, job_title, job_type, job_location, url):
    """CLI tool for searching students jobs in Israel, designed for students by students"""

    if not resource:
        # get_linkedin(url=url)
        get_indeed(job_title=job_title, job_location=job_location)
        get_glassdoor(job_title=job_title, job_type=job_type, job_location=job_location)

    else:
        resource = resource.lower().strip()
        
    if resource == 'linkedin':
        if url:
            get_linkedin(url=url)
        else:
            click.echo('Linkedin resource requires job url input.')

    elif resource == 'glassdoor':
        get_glassdoor(job_title=job_title, job_type=job_type, job_location=job_location)

    elif resource == 'indeed':
        if job_location:
            get_indeed(job_title=job_title, job_location=job_location)
        else:
            click.echo('Indeed resource requires job location input.')
    
    else:
        click.echo(f'{resource} is not a valid resource.')


if __name__ == '__main__':
    cli_get_jobs()
