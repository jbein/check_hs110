# check_hs110
Plugin for Icinga2 to check a TP Link HS110 Smartplug

## CheckCommand definition for icinga2

object CheckCommand "check_hs110" {
        import "plugin-check-command"

        command = [ PluginDir + "/check_hs110.py" ]

        arguments = {
                "-H" = "$address$"
        }
}

