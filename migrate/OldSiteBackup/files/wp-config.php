<?php

define('FS_METHOD', 'direct');

/**
 * The base configuration for WordPress
 *
 * The wp-config.php creation script uses this file during the
 * installation. You don't have to use the web site, you can
 * copy this file to "wp-config.php" and fill in the values.
 *
 * This file contains the following configurations:
 *
 * * MySQL settings
 * * Secret keys
 * * Database table prefix
 * * ABSPATH
 *
 * @link https://codex.wordpress.org/Editing_wp-config.php
 *
 * @package WordPress
 */

// ** MySQL settings ** //
/** The name of the database for WordPress */
define( 'DB_NAME', 'dbs10271854' );

/** MySQL database username */
define( 'DB_USER', 'dbu1695866' );

/** MySQL database password */
// define( 'DB_PASSWORD', getenv('DB_PASSWORD') );
define( 'DB_PASSWORD', 'F*ckOffDarwall' );

/** MySQL hostname */
define( 'DB_HOST', 'db5012206910.hosting-data.io' );

/** Database Charset to use in creating database tables. */
define( 'DB_CHARSET', 'utf8' );

/** The Database Collate type. Don't change this if in doubt. */
define( 'DB_COLLATE', '' );

/**
 * Authentication Unique Keys and Salts.
 *
 * Change these to different unique phrases!
 * You can generate these using the {@link https://api.wordpress.org/secret-key/1.1/salt/ WordPress.org secret-key service}
 * You can change these at any point in time to invalidate all existing cookies. This will force all users to have to log in again.
 *
 * @since 2.6.0
 */
define('AUTH_KEY',         '3S[A[eI4 i_uM|xxX+?K@C?lb+2dV|4g.Q09]_W8X6(v/A.%jkR+>5^=fcKE87N^');
define('SECURE_AUTH_KEY',  '.(/3s6JYg|^cZJ)n3Vm&yZ}<:9e?H:oYuoyk|1.[:30Of/Q=YNBuyTDGoP>_B3)F');
define('LOGGED_IN_KEY',    'oy[3g%.UQ;56-^RXbB!c)W$@>*#l>7Ey6ygjFj1zlTiD30^0)*l|O/bHFOII7hpm');
define('NONCE_KEY',        'fP+.Jg|]*vvo-3h$i20+M>O%:v=Ch0+xY|O[D&c/KsLI!W4;i%p+$@=-GsRL_cMc');
define('AUTH_SALT',        'q. $#!3b3nSEHoDi+a@>tB;|7$o|~Oti78|ndi0,a`Jc 89ebR&~H~g?ef9Wjf/}');
define('SECURE_AUTH_SALT', 'S#9:3jbl/>$Vt.NiuzhZod;Df2`|0yKRp?qG&~A-l6]M6PX|*Vmtc&tG=M_,c6Nb');
define('LOGGED_IN_SALT',   '+}IU^3kHP*UHUSB#-|u`+WAbrN{MV+Ak>#e)uPlXO-b>xZ^Lu8/:8x;~%|^r)Kt5');
define('NONCE_SALT',       'QI[:-psMQBE>a0{Yw~&4d-i)>M>UYhmoH.zhwj+5&mCTlf{D4^]=.D`PW`{LIzb*');


/**
 * WordPress Database Table prefix.
 *
 * You can have multiple installations in one database if you give each
 * a unique prefix. Only numbers, letters, and underscores please!
 */
$table_prefix = 'KvmJVdYH';




/* That's all, stop editing! Happy blogging. */

/** Absolute path to the WordPress directory. */
if ( ! defined( 'ABSPATH' ) )
	define( 'ABSPATH', dirname( __FILE__ ) . '/' );

/** Sets up WordPress vars and included files. */
require_once ABSPATH . 'wp-settings.php';
