#!/usr/bin/env python3
# -*- coding: utf8 -*-

import argparse

def create_argument_parser():
	arg_parser = argparse.ArgumentParser(
			prog='hide_my_python',
			description='A parser to retrieve proxies from HideMyAss!',
			epilog='Go to https://hidemyass.com/proxy-list/ to see the\
					different available options.')

	# The user has to specify an output file
	arg_parser.add_argument('-o', dest='database_file', type=str,
			required=True,
			help='database file where the proxies will be saved')

	# The user can specify a maximum number of proxies to retrieve
	arg_parser.add_argument('-n', dest='number_of_proxies', type=int,
			default=0,
			help='maximum number of proxies to retrieve (default: all')

	# The user can specify a list of countries
	arg_parser.add_argument('-ct', default='countries_all',
			dest='countries_file', type=argparse.FileType('r'),
			help='file containing the countries where the\
					proxies can be based (default: %(default)s)')

	# The user can specify a list of ports
	arg_parser.add_argument('-p', type=int, nargs='+', dest='ports',
			help='list of ports (max: 20 ports) the proxies listen on\
					(default: every port)')

	# The user can specify a list of protocols
	arg_parser.add_argument('-pr', type=str, nargs='+',
			choices=['http', 'https', 'socks'], dest='protocols',
			help='protocols used by the proxies\
					(default: HTTP, HTTPS and SOCKS4/5)')

	# The user can specify the anonymity level
	arg_parser.add_argument('-a', default=0, action='count', dest='anonymity',
			help='flag used to determine the proxies minimum anonymity\
					level, e.g. -a sets the minimum anonymity level to Low,\
					-aa to Medium, -aaa to High, etc. (default minimum level:\
					None)')

	arg_parser.add_argument('-ka', action='store_true',
			dest='keep_alive',
			help='flag used to determine if proxies with the Keep Alive\
					option should be returned, as they are likely honey pots\
					(default: no)')

	# The user can specify the required speed
	arg_parser.add_argument('-s', default=1, action='count', dest='speed',
			help='flag used to determine the proxies minimum speed\
					level, e.g. -s sets the minimum speed level to Medium,\
					-ss to Fast (default minimum level: Slow)')

	# The user can specify the connection time
	arg_parser.add_argument('-c', default=1, action='count',
			dest='connection_time',
			help='flag used to determine the proxies minimum connection time\
					level, e.g. -c sets the minimum connection time level to\
					Medium, -cc to Fast (default minimum level: Slow)')

	return arg_parser

def process_arguments(args, arg_parser):

	# If the given number of proxies is negative,
	# we return an error
	if args.number_of_proxies < 0:
		error_msg = '{0}: error: argument {1}: invalid value '\
				+ '(a positive integer is required): {2}'
		error_msg = error_msg.format(arg_parser.prog, '-n',
				args.number_of_proxies)
		arg_parser.error(error_msg)

	# We retrieve the countries from the given file
	args.countries_list = []
	for country in args.countries_file.readlines():
		country = country.rstrip()
		args.countries_list.append(country)

	# If ports were specified
	if args.ports:
		# We delete the duplicates
		args.ports = list(set(args.ports))
		# If too many ports were specified, we exit with an error
		if len(args.ports) > 20:
			error_msg = '{0}: error: argument {1}: invalid value '\
					+ '(maximum 20 ports): {2} ports given'
			error_msg = error_msg .format(arg_parser.prog, '-p',
					len(args.ports))
			arg_parser.error(error_msg)
		# Otherwise, we create a comma-separated string
		else:
			ports_string = ''
			for port in args.ports:
				# If the port is in the good range, we add it
				if 1 <= port and port <= 65535:
					ports_string += '{0}, '.format(port)
				# Otherwise, we raise an error
				else:
					error_msg = '{0}: error: argument {1}: invalid value '\
							+ '(port must be between 1 and 65535): {2}' 
					error_msg = error_msg .format(arg_parser.prog, '-p',
							port)
					arg_parser.error(error_msg)
				# We delete the last comma
				ports_string = ports_string[:-2]
				args.ports = ports_string
	# If no ports were specified, we do nothing
	else:
		args.ports = ''

	# If no protocol was specified, we consider every possible protocol
	if not args.protocols:
		args.protocols = ['http', 'https', 'socks']
	# Otherwise, we delete the duplicates
	else:
		args.protocols = list(set(args.protocols))

	# The maximum anonymity level is 4
	if args.anonymity > 4:
		args.anonymity = 4

	# The maximum speed level is 3
	if args.speed > 3:
		args.speed = 3

	# The maximum connection time level is 3
	if args.connection_time > 3:
		args.connection_time = 3

