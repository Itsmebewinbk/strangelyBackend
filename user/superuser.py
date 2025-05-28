import click
from user.models import User
from db import get_sync_db
# from app.logger_settings import get_logger

# admin_logger = get_logger("admin")

@click.command()
@click.option("--superadmin", is_flag=True, help="Create a superadmin.")
@click.argument("email", required=False)
@click.argument("password", required=False)
def create_admin(superadmin, email, password):
    """
    Command to create a new admin user.
    Usage examples:
        - Interactive:  python -m user.superuser
`

        With parameters:
        - Admin:        `python -m app.admin.cli user pass`
        - Superadmin:   `python -m app.admin.cli --superadmin user pass`
    """
    if not email:
        email = click.prompt("Enter email").strip().lower()
    if not password:
        password = click.prompt("Enter password", hide_input=True)
        confirm_password = click.prompt("Confirm password", hide_input=True)
        if password != confirm_password:
            click.echo("Passwords don't match. Try again!")
            return

   

    db = next(get_sync_db())
    try:
        existing_admin = db.query(User).filter_by(email=email,is_superuser=True).first()
        if existing_admin:
            click.echo("Username already exists!")
            # admin_logger.warning(
            #     {
            #         "event" : "Username already exists!",
            #         "username" : username
            #     }
            # )
            return
        new_admin = User(
            email=email, is_superuser=True,firebase_token="admin-cli-generated",
        )
        new_admin.set_password(password)
        db.add(new_admin)
        db.commit()
        # admin_logger.info(
        #     {
        #         "event" : "Admin created successfully.",
        #         "admin_id" : new_admin.id,
        #         "email" : email,
        #         "super_admin_status" : superadmin
        #     }
        # )
        click.echo("Admin user created successfully!")

    except Exception as e:
        db.rollback()
        # admin_logger.error(
        #     {
        #         "event" : "Admin creation failed!",
        #         "username" : username
        #     }
        # )
        click.echo(f"Error: {e}")

    finally:
        db.close()


if __name__ == "__main__":
    create_admin()