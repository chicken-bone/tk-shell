import os
import sys


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def start_toolkit():
    """
    Import Toolkit and start up a tk-shell engine based on
    environment variables.
    """

    # Verify sgtk can be loaded.
    try:
        import sgtk
    except Exception as e:
        print "Shotgun: Could not import sgtk! Disabling for now: {}".format(e)
        return

    # start up toolkit logging to file
    sgtk.LogManager().initialize_base_file_handler("tk-shell")
    logger = sgtk.LogManager.get_logger(__name__)

    logger.debug("Launching toolkit in classic mode.")

    # Get the name of the engine to start from the environement
    env_engine = os.environ.get("SGTK_ENGINE")
    if not env_engine:
        print "Shotgun: Missing required environment variable SGTK_ENGINE."
        return

    # Get the context load from the environment.
    env_context = os.environ.get("SGTK_CONTEXT")
    if not env_context:
        print "Shotgun: Missing required environment variable SGTK_CONTEXT."
        return
    try:
        # Deserialize the environment context
        context = sgtk.context.deserialize(env_context)
    except Exception as e:
        print "Shotgun: Could not create context! Shotgun Pipeline Toolkit will " \
              "be disabled. Details: {}".format(e)
        return

    try:
        # Start up the toolkit engine from the environment data
        logger.debug(
            "Launching engine instance '%s' for context %s" % (env_engine, env_context)
        )
        print "Bootstrapping Toolkit, please hang on a second..."

        engine = sgtk.platform.start_engine(env_engine, context.sgtk, context)
        new_globals = {
            "tk": engine.sgtk,
            "shotgun": engine.shotgun,
            "context": engine.context,
            "engine": engine,
        }
        globals_dict = globals()
        globals_dict.update(new_globals)

        welcome_message = (
            "Welcome to the Shotgun Python Console!\n\n"
            "Python {}\n\n"
            "- A tk API handle is available via the 'tk' variable\n"
            "- A Shotgun API handle is available via the 'shotgun' variable\n"
            "- Your current context is stored in the 'context' variable\n"
            "- The shell engine can be accessed via the 'engine' variable\n\n"
            .format(sys.version,)
        )
        cls()
        print welcome_message
        return
        # subprocess.Popen(os.environ.get("SGTK_TERMINAL"), shell=True, env=os.environ)
    except Exception as e:
        print "Shotgun: Could not start engine: {}".format(e)
        return

    # # Clean up temp env variables.
    # del_vars = [
    #     "SGTK_ENGINE",
    #     "SGTK_CONTEXT",
    # ]
    # for var in del_vars:
    #     if var in os.environ:
    #         del os.environ[var]


if __name__ == "__main__":
    start_toolkit()
